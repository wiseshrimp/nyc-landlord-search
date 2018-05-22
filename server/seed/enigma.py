# -*- coding: utf-8 -*-

# TO DO:
  # import landlord data, search landlord by building id and associate each building with landlord
  # still solve for case in which there's a stall
  # can you run multiple instances at once? will that speed things up?
  # simultaneously check for likelihood of rent controlled apartment
#

# -*- coding: utf-8 -*-
import unidecode
import requests
# from flask import Flask, request
import flask
import json
from threading import Timer

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import psycopg2
import json

from constants import BASE_URL, ENIGMA_PARAMS, CREATE_QUERY, DEFAULT_TITLE, PROPERTY_PROFILE_TITLE
from driver import *
from building import Building

class Populator:
  def __init__(self, snapshot_id, is_db_set):
    self.snapshot_id = snapshot_id
    self.has_restarted = False
    self.current_idx = 0
    self.row_offset = 50
    self.row_limit = 100
    if is_db_set != True:
      self.build_db()
    self.populate()
  
  def build_db(self):
    cur.execute(CREATE_QUERY)
  
  def get_enigma_data(self):
    url = ENIGMA_PARAMS.format(
      BASE_URL,
      self.snapshot_id,
      self.row_offset,
      self.row_limit
    )
    r = requests.get(
      url,
      headers = headers
    )
    dataset = r.json()
    # number of rows, max = 10000 for engima query
    row_count = dataset['current_snapshot']['row_count']
    self.data = dataset['current_snapshot']['table_rows']['rows']

  def populate(self):
    if self.has_restarted:
      self.row_offset = self.current_idx
      self.has_restarted = False
    
    self.get_enigma_data()

    for address in self.data:
      building = Building(address)
      building.get_bis()
      if driver.title != DEFAULT_TITLE:
        print("Overworked server. Starting again.")
        while driver.title != DEFAULT_TITLE:
          timer = Timer(1.0, building.get_bis)
          timer.start()
      building.get_bis_data()
      if driver.title != PROPERTY_PROFILE_TITLE:  # listing not found -- move to next index
        print("Listing does not exist in BIS network")
        continue  # exit out of loop and proceed to next entry
      building.get_building_id()
      
      is_duplicate = building.check_if_duplicate()
      if is_duplicate:
        print("Duplicate entry: #{}".format(building.building_id))
        continue
      
      building.get_lat_long_coordinates()
      building.get_complaints_and_violations()      
      building.post_data()
      driver.quit()
    

  # TO DO: Divide number of entries by 10,000 (query limit) loop through

populator = Populator('e895e31c-7233-4474-bc4d-889eee172a8b', True)

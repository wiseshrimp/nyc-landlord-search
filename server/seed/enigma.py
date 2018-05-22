# TO DO:
  # import landlord data, search landlord by building id and associate each building with landlord
  # still solve for case in which there's a stall
  # can you run multiple instances at once? will that speed things up?
  # simultaneousy check for likelihood of rent controlled apartment
  
#


# -*- coding: utf-8 -*-
import unidecode
import requests
# from flask import Flask, request
import flask
import json
from geopy.geocoders import Nominatim
from threading import Timer

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import psycopg2
import json

from constants import *
from db import *

# app = Flask(__name__)
driver = webdriver.Chrome("/Users/sueroh/chromedriver")
geolocator = Nominatim()
hasRestarted = False

# Connect to an existing database
conn = psycopg2.connect("dbname=landlord-dev user=postgres")

# Open a cursor to perform database operations
cur = conn.cursor()

class Populator:
  def __init__(self, snapshot_id, isDbSetup):
    self.snapshot_id = snapshot_id
    self.has_restarted = False
    self.current_idx = 0
    self.row_offset = 50
    self.row_limit = 100
    if isDbSetup != True: self.buildDb()

    self.populate()
  
  def buildDb(self):
    cur.execute(CREATE_QUERY)

  def populate(self):
    if self.has_restarted:
      self.row_offset = self.current_idx
      self.has_restarted = False
    url = """
      {}datasets/{}?
      &row_offset={}
      &row_limit={}
    """.format(BASE_URL, self.snapshot_id, self.row_offset, self.row_limit)
    r = requests.get(url, headers=headers)
    dataset = r.json()
    # number of rows, max = 10000 for engima query
    row_count = dataset['current_snapshot']['row_count']
    data = dataset['current_snapshot']['table_rows']['rows']

    for address in data:
      self.assign_values(address)
      self.get_bis()
      if driver.title != "DOB Building Information Search":
        print("Overworked server, starting again...")

      self.get_bis_data()
      if driver.title != "Property Profile Overview":  # listing not found -- move to next index
        print("Listing does not exist in BIS network")
        continue  # exit out of loop and proceed to next entry
      self.get_building_id()

      is_duplicate = self.check_for_duplicates()
      if is_duplicate:
        continue
      self.get_coordinates()
      self.get_complaints_and_violations()
      self.post_data()

  def assign_values(self, address):
    self.borough = BOROUGHS[int(address[0]) - 1]
    addressArr = address[8].split(' ', 1)
    self.building_number = addressArr[0]
    self.street_name = addressArr[1]
    self.block_number = address[4]
    self.neighborhood = address[1]
    self.zip_code = int(address[10])
    self.year_built = int(address[16])
    self.sale_price = address[19]
    self.sale_date = address[20]
  
  def get_bis(self):
    driver.get(BIS_LINK)
  
  def get_bis_data(self):
    boroughSelect = driver.find_element_by_id("boro1")
    for option in boroughSelect.find_elements_by_tag_name("option"):
      if option.text == self.borough:
          option.click()
          break
    driver.find_element_by_name("houseno").send_keys(self.building_number)
    driver.find_element_by_name("street").send_keys(self.street_name)
    driver.find_element_by_name("go2").click()


  def get_coordinates(self):
    full_address = "{} {}, {}, NY, {}".format(self.building_number, self.street_name, self.borough, self.zip_code)
    location = geolocator.geocode(full_address)
    if location == None:
      self.on_error("Location error: Address coordinates not found – {}".format(full_address))
      return
    self.latitude = location.latitude
    self.longitude = location.longitude

  def get_building_id(self):
    textEl = driver.find_element_by_xpath(
      "//td[contains(@class, 'maininfo')][@align='right']")
    innerText = textEl.get_attribute("innerText")
    innerTextASCII = unidecode.unidecode(innerText)
    innerTextArr = innerTextASCII.split(' ')
    self.building_id = int(innerTextArr[2])

  def get_complaints_and_violations(self):
    self.num_of_complaints = 0
    self.num_of_dob_violations = 0
    self.num_of_ecb_violations = 0
    self.complaints_link = None
    self.dob_violations_link = None
    self.ecb_violations_link = None
    aNodes = driver.find_elements_by_tag_name("a")
    for node in aNodes:
      if "Violations-DOB" in node.text:
        violationNumberNode = driver.find_element_by_xpath(
            "//html/body/center/table[8]/tbody/tr/td[1]/table/tbody/tr[3]/td[2]"
        )
        self.num_of_dob_violations = int(violationNumberNode.text)
        self.dob_violations_link = node.get_attribute("href")
      if "Violations-ECB" in node.text:
        violationECBNumberNode = driver.find_element_by_xpath(
            "//html/body/center/table[8]/tbody/tr/td[1]/table/tbody/tr[4]/td[2]"
        )
        self.num_of_ecb_violations = int(violationECBNumberNode.text)
        self.ecb_violations_link = node.get_attribute("href")
      if "Complaints" in node.text:
        complaintNumberNode = driver.find_element_by_xpath(
            "//html/body/center/table[8]/tbody/tr/td[1]/table/tbody/tr[2]/td[2]"
        )
        self.num_of_complaints = int(complaintNumberNode.text)
        self.complaints_link = node.get_attribute("href")
  def post_data(self):
    post_query = """INSERT INTO buildings ({}) 
      VALUES ({}); """.format(
        FIELDS_TEXT,
        FIELD_VARIABLES
      )
    cur.execute(post_query.format(
        self.building_id,
        self.building_number,
        self.street_name,
        self.zip_code,
        self.neighborhood,
        self.borough,
        self.latitude,
        self.longitude,
        self.block_number,
        self.year_built,
        self.sale_price,
        self.sale_date,
        self.num_of_complaints,
        self.num_of_dob_violations,
        self.num_of_ecb_violations,
        self.complaints_link,
        self.dob_violations_link,
        self.ecb_violations_link))
    conn.commit()
    # driver.quit()

  def check_for_duplicates(self):
      # Check if address already exists in db
      # TO DO: Compare complaint / violation numbers?
    cur.execute("""
      SELECT COUNT(*)
      FROM buildings
      WHERE building_id = {}
      """.format(self.building_id))
    rows = cur.fetchall()
    count = rows[0][0]
    return count > 0

  def on_error(self, err_message):
    print("Error: {}".format(err_message))
    

  # TO DO: Divide number of entries by 10,000 (query limit) loop through

populator = Populator('e895e31c-7233-4474-bc4d-889eee172a8b', True)

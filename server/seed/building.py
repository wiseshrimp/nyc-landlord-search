# -*- coding: utf-8 -*-

import unidecode
from geopy.geocoders import Nominatim
from threading import Timer

from driver import driver
from constants import *

geolocator = Nominatim()

class Building:
  def __init__(self, address):
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
  
  def get_building_id(self):
    textEl = driver.find_element_by_xpath(BUILDING_ID_XPATH)
    innerText = textEl.get_attribute("innerText")
    innerTextASCII = unidecode.unidecode(innerText)
    innerTextArr = innerTextASCII.split(' ')
    self.building_id = int(innerTextArr[2])
  
  def check_if_duplicate(self): # Checks if building_id is already in db because enigma data has duplicates
      # TO DO: Compare complaint / violation numbers?
    cur.execute(DUPLICATE_COUNT_QUERY.format(self.building_id))
    rows = cur.fetchall()
    count = rows[0][0]
    return count > 0

  def get_lat_long_coordinates(self):
    full_address = ADDRESS_COORDINATES_PARAMS.format(
        self.building_number,
        self.street_name,
        self.borough,
        self.zip_code
    )
    location = geolocator.geocode(full_address)
    if location == None:
      self.on_error(
          "Location error: Address coordinates not found – {}".format(full_address))
      return
    self.latitude = location.latitude
    self.longitude = location.longitude
  
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
          DOB_VIOLATIONS_XPATH)
        self.num_of_dob_violations = int(violationNumberNode.text)
        self.dob_violations_link = node.get_attribute("href")
      elif "Violations-ECB" in node.text:
        violationECBNumberNode = driver.find_element_by_xpath(
            ECB_VIOLATIONS_XPATH)
        self.num_of_ecb_violations = int(violationECBNumberNode.text)
        self.ecb_violations_link = node.get_attribute("href")
      elif "Complaints" in node.text:
        complaintNumberNode = driver.find_element_by_xpath(COMPLAINT_XPATH)
        self.num_of_complaints = int(complaintNumberNode.text)
        self.complaints_link = node.get_attribute("href")

  def post_data(self):
    post_query = POST_BUILDING_QUERY.format(
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
        self.ecb_violations_link
    ))
    conn.commit()
  
  def on_error(self, err_message):
    print("Error: {}".format(err_message))

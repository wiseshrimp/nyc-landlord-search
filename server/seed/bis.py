from selenium import webdriver
from selenium.webdriver.common.keys import Keys
bisLink = "http://a810-bisweb.nyc.gov/bisweb/bispi00.jsp"

driver = webdriver.Chrome("/Users/sueroh/chromedriver")
driver.get(bisLink)

# BIS BUILDING INFORMATION SEARCH
assert "DOB Building Information Search" in driver.title
boroughSelect = driver.find_element_by_id("boro1")
for option in boroughSelect.find_elements_by_tag_name("option"):
  if option.text == "Brooklyn":
      option.click()
      break
houseNoInput = driver.find_element_by_name("houseno")
houseNoInput.send_keys("74")
streetInput = driver.find_element_by_name("street")
streetInput.send_keys("Macdonough Street")
submitButton = driver.find_element_by_name("go2")
submitButton.click()
# print("HELLOOOOOO")

# END OF BIS BUILDING INFORMATION SEARCH

# driver.close()

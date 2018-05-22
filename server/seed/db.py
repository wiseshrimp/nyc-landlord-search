import psycopg2
import json
from constants import *
# Connect to an existing database
conn = psycopg2.connect("dbname=landlord-dev user=postgres")

# Open a cursor to perform database operations
cur = conn.cursor()

# class Database:
#   def __init__(self, data):
    

# def buildDatabase():
#   # Execute a command: this creates a new table
#   cur.execute(CREATE_QUERY)

# # last_index = 0

# def populateDatabase(data):
#   # Check if address already exists in db
#   # TO DO: Compare complaint / violation numbers?
#   cur.execute("""
#     SELECT COUNT(*)
#     FROM buildings
#     WHERE building_id = {}
#     """.format(data["building_id"]))
#   rows = cur.fetchall()
#   count = rows[0][0]
#   if count > 0:
#     return

#   cur.execute("""
#     INSERT INTO buildings 
#       ({}) VALUES ({}); """.format(
#           FIELDS_TEXT,
#           FIELD_VARIABLES,
#           data["building_id"],
#           data["building_number"],
#           data["street_name"],
#           data["zip_code"],
#           data["neighborhood"],
#           data["borough"],
#           data["latitude"],
#           data["longitude"],
#           data["block_number"],
#           data["year_built"],
#           data["sale_price"],
#           data["sale_date"],
#           data["num_of_complaints"],
#           data["num_of_dob_violations"],
#           data["num_of_ecb_violations"],
#           data["complaints_link"],
#           data["dob_violations_link"],
#           data["ecb_violations_link"]))

# # Make the changes to the database persistent
#   conn.commit()

# # Close communication with the database


# def closeDbConnection():
#   cur.close()
#   conn.close()

# # buildDatabase()

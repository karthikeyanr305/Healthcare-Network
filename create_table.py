import random

import csv
import psycopg2
from faker import Faker
Faker.seed(33422)

fake = Faker()

try:
  conn = psycopg2.connect(
    host="localhost",
    database="Hospital",
    user="chris", # Change user
    password="") # Change password
  cursor = conn.cursor()

  with open('accidents.csv', 'r') as f:
    n = 0
    reader = csv.reader(f)
    next(reader) # Skip the header row.
    accidentIdArray = []
    zipcodeArray = []
    for row in reader:
      n += 1
      if n==10000:
        break
      if (row[16].replace("'", '"') != ''):
        zipcodeArray.append(row[16].replace("'", '"'))
        cursor.execute(
          "INSERT INTO zipcodeDetails VALUES ('%s', '%s', '%s', '%s') ON CONFLICT (zipcode) DO NOTHING"
        % (row[16].replace("'", '"'), row[15].replace("'", '"'), row[13].replace("'", '"'), row[14].replace("'", '"')))
        print("zipcode inserted", row[16])

        accidentIdArray.append(row[0].replace("'", '"'))
        cursor.execute(
          "INSERT INTO accidents VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') ON CONFLICT (accident_id) DO NOTHING"
        % (row[0].replace("'", '"'), row[1].replace("'", '"'), row[2].replace("'", '"'), row[4].replace("'", '"'), row[5].replace("'", '"'), row[11].replace("'", '"'), row[12].replace("'", '"'), row[16].replace("'", '"')))

  hospitalIdArray = []
  with open('hospital.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # Skip the header row.
    for row in reader:
      hospitalIdArray.append(row[3].replace("'", '"'))
      cursor.execute(
        "INSERT INTO hospitalDetails VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') ON CONFLICT (hospital_id) DO NOTHING"
      % (row[3].replace("'", '"'), row[4].replace("'", '"'), row[5].replace("'", '"'), row[8].replace("'", '"'), row[10].replace("'", '"'), row[11].replace("'", '"'), row[31].replace("'", '"'), row[33].replace("'", '"')))

      cursor.execute(
        "INSERT INTO hospitalLocation VALUES ('%s', '%s', '%s') ON CONFLICT (hospital_id) DO NOTHING"
      % (row[3].replace("'", '"'), row[17].replace("'", '"'), row[18].replace("'", '"')))

  cursor.execute(" \
    INSERT INTO bloodGroup (blood_group_id, blood_group) \
    VALUES ('A', 'AB+'), ('B', 'AB-'), ('C', 'A+'), ('D', 'A-'), ('E', 'B+'), ('F', 'B-'), ('G', 'O-'), ('H', 'O+') ON CONFLICT (blood_group_id) DO NOTHING;")
  print("Inserted bloodGroup")

  bloodIdArray = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
  for el in hospitalIdArray:
    for i in range(random.randint(3, 8)):
      cursor.execute(" \
        INSERT INTO bloodAvailability (blood_group_id, hospital_id, quantity) \
        VALUES ('%s', '%s', %s) ON CONFLICT (blood_group_id, hospital_id) DO NOTHING;"
        % (random.choice(bloodIdArray), el, random.randint(500, 2000)))
  print("Inserted bloodAvailability")

  cursor.execute(" \
    INSERT INTO organ (organ_id, organ) \
    VALUES ('O1', 'Kidney'), ('O2', 'Liver'), ('O3', 'Heart'), ('O4', 'Lung'), ('O5', 'Pancreas'), ('O6', 'Small bowel');")
  print("Inserted organ")

  donorlist = []
  for i in range(10000):
    row = fake.simple_profile()
    donor = 'DO' + str(i)
    donorlist.append(donor)
    cursor.execute(" \
      INSERT INTO donor (donor_id, name, age, sex, address, zipcode, phone) \
      VALUES ('%s', '%s', %s, '%s', '%s', %s, '%s'); \
      " % (donor, row['name'], fake.random_int(0, 80), row['sex'], row['address'], random.choice(zipcodeArray), fake.random_int(1000000000, 10000000000)))
  print("Inserted donor")

  for el in hospitalIdArray:
    for i in range(random.randint(0, 6)):
      cursor.execute(" \
        INSERT INTO organAvailability (organ_id, hospital_id, quantity) \
        VALUES ('%s', '%s', %s) ON CONFLICT (organ_id, hospital_id) DO NOTHING;"
        % (random.choice(['O1', 'O2', 'O3', 'O4', 'O5', 'O6']), el, random.randint(1, 5)))
  print("Inserted organAvailability")

  for el in donorlist:
    for i in range(random.randint(1, 4)):
      cursor.execute(" \
        INSERT INTO organDonor (organ_id, donor_id) \
        VALUES ('%s', '%s') ON CONFLICT (organ_id, donor_id) DO NOTHING;"
        % (random.choice(['O1', 'O2', 'O3', 'O4', 'O5', 'O6']), el))
  print("Inserted organDonor")

except Exception as e:
  print ("Unknown error", e)
finally:
#closing database connection.
  if(conn):
    conn.commit()
    cursor.close()
    conn.close()
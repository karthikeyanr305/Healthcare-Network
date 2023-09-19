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

#   ('A', 'AB+'), ('B', 'AB-'), ('C', 'A+'), ('D', 'A-'), ('E', 'B+'), ('F', 'B-'), ('G', 'O-'), ('H', 'O+')

  bloodIdArray = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
  blood = ['AB+', 'AB-', 'A+', 'A-', 'B+', 'B-', 'O-', 'O+']

  cursor.execute("Insert into AccidentHospital SELECT DISTINCT accident_id, hospital_id, distance FROM (SELECT accident_id, hospital_id, distance, rank() over (partition by accident_id order by (distance)) as distance_rank FROM(SELECT accident_id, hospital_id, findDistance(accident_latitude, accident_longitude, hospital_latitude, hospital_longitude) as distance FROM (SELECT * FROM accidents NATURAL JOIN zipcodedetails) as A INNER JOIN (SELECT * FROM hospitalLocation NATURAL JOIN hospitaldetails NATURAL JOIN zipcodedetails) as B ON A.city = B.city) as C) as WHERE distance_rank = 1;")

  cursor.execute("Select accident_id, hospital_id from AccidentHospital")
  records = cursor.fetchall()

  for i in range(10000):
    row = fake.simple_profile()
    patient = 'PA' + str(i)
    bloodPosition = random.randint(0, 7)
    cursor.execute(" \
      INSERT INTO patientDetails (patient_id, name, age, sex, address, phone, blood_group) \
      VALUES ('%s', '%s', %s, '%s', '%s', '%s', '%s'); \
      " % (patient, row['name'], fake.random_int(0, 80), row['sex'], row['address'], fake.random_int(1000000000, 10000000000), blood[bloodPosition]))

    accidentHospital = random.choice(records)

    cursor.execute("INSERT INTO patientAccident (patient_id, accident_id, hospital_id) \
        VALUES ('%s', '%s', '%s');" %(patient, accidentHospital[0], accidentHospital[1]))

    if random.choice([0, 1, 0]):
        cursor.execute("INSERT INTO patientBlood (patient_id, blood_group_id, quantity) \
            VALUES ('%s', '%s', %s);" %(patient, bloodIdArray[bloodPosition], random.randint(50, 200)))

    if random.choice([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]):
        cursor.execute("INSERT INTO patientOrgan (patient_id, organ_id, quantity) \
            VALUES ('%s', '%s', 1);" %(patient, random.choice(['O1', 'O2', 'O3', 'O4', 'O5', 'O6'])))

except Exception as e:
  print ("Unknown error", e)
finally:
#closing database connection.
  if(conn):
    conn.commit()
    cursor.close()
    conn.close()
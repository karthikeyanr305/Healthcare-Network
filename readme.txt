Accident dataset downloaded from https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents
Hospital dataset downloaded from https://www.kaggle.com/datasets/andrewmvd/us-hospital-locations

Steps for running the project
1. Run sql file project_ddl.sql for creating the relations
2. Run the python script initial_populate_table.py for populating data from datasets
3. Run the sql file distanceFunction.sql for creating a function
4. Populate accidenthospital relation and patient relation using populate_patient.py
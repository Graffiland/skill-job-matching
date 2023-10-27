import pandas as pd
import sqlite3
from transform import masked_text, masked_survey
import json


conn = sqlite3.connect('mydatabase.db')

cursor = conn.cursor()

cursor.execute('''DROP TABLE skilljob''')

# Create the energy_data table with the specified columns
cursor.execute('''CREATE TABLE skilljob (
     maskedcv TEXT CHECK(LENGTH(maskedcv) <= 1000000000),    
     maskedsurvey JSON CHECK(LENGTH(maskedsurvey) <= 10000000000)      
                 )''')

# masked_survey_dict = json.loads(masked_survey)

# Insert data into the table

cursor.executemany("INSERT INTO skilljob(maskedcv) VALUES (?)", [
                   (value,) for value in masked_text])

# cursor.execute(
#     "UPDATE skilljob SET maskedsurvey = ?", (masked_survey,))

cursor.execute('''SELECT * FROM skilljob''')

# Fetch all rows
rows = cursor.fetchall()

print(rows)

# Print the column names (assuming you want to print them)
column_names = [description[0] for description in cursor.description]
print(column_names)

# Print data in each column for each row
for row in rows:
    print(row)

# Save the changes and close the connection
conn.commit()
conn.close()

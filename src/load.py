import sqlite3
import json
from transform import masked_text, masked_survey

# Connect to the SQLite database
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# Drop the table if it exists (optional)
cursor.execute('''DROP TABLE IF EXISTS skilljob''')

# Create the skilljob table with the specified columns
cursor.execute('''CREATE TABLE skilljob (
    maskedcv TEXT CHECK(LENGTH(maskedcv) <= 1000000000),
    maskedsurvey JSON CHECK(LENGTH(maskedsurvey) <= 10000000000)
)''')

# Insert data into the table
insert_data = [
    (masked_text, json.dumps(masked_survey)),
    # Add more rows as needed
]

cursor.executemany("INSERT INTO skilljob (maskedcv, maskedsurvey) VALUES (?, ?)", insert_data)

# Commit the changes
conn.commit()

# Retrieve and display data
cursor.execute("SELECT * FROM skilljob")
rows = cursor.fetchall()

# Print the column names
column_names = [description[0] for description in cursor.description]
print(column_names)

# Print data in each column for each row
for row in rows:
    print(row)

## alternative way of printing all rows
##for row in cursor.execute(select * from skilljob):
#      print(row)
# Close the connection
conn.close()

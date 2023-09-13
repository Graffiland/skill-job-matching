import pandas as pd
import sqlite3

conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

cursor.execute('''DROP TABLE Data''')

# Create the energy_data table with the specified columns
cursor.execute('''CREATE TABLE Data (
                   
                 )''')
 


cursor.execute('''SELECT * FROM Data''')

rows = cursor.fetchall()
for row in rows:
    print(row)

# Save the changes and close the connection
conn.commit()
conn.close()

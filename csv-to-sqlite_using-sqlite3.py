import csv
import sqlite3


"""

# Here is one way from: "How to Import a CSV file into a SQLite database Table using Python" at 
# https://www.geeksforgeeks.org/how-to-import-a-csv-file-into-a-sqlite-database-table-using-python/#
# 
# and see https://dnmtechs.com/importing-csv-data-into-sqlite-database-with-python-3/ 
# for skipping the 1st row of the csv file when it includes column names.

# Connecting to the LC ECD database
connection = sqlite3.connect('ecd.db')

# Create a cursor object to execute
# SQL queries against a database table
cursor = connection.cursor()

# Table Definition (https://sqlite.org/datatype3.html)
# Datatypes In SQLite databases are "Storage Classes": 
#    NULL, INTEGER, REAL, TEXT and BLOB
# [REAL: only the first 15 significant decimal digits of the number are preserved]
# and columns have "type affinity":
#    TEXT, NUMERIC, INTEGER, REAL and BLOB
# A TEXT DateTime is stored as ISO8601 strings ("YYYY-MM-DD HH:MM:SS.SSS").
#    See: https://sqlite.org/lang_datefunc.html to use them.


# https://sqlitebrowser.org/dl/#windows
# or in your browser:
# https://inloop.github.io/sqlite-viewer/
#
# how to create a date field in an sqlite database
# https://duckduckgo.com/?t=h_&q=how+to+create+a+date+field+in+an+sqlite+database&ia=web
#
# https://sqlite.org/pragma.html#pragma_index_info
# Built-in Aggregate Functions
# https://www.sqlite.org/lang_aggfunc.html


# After your csv file is converted into an sqlite database, you can use SQL to extract data.
# Here in this case it created with file name “ecd.db”

# import sqlite3
# con=sqlite3.connect('ecd.db')
# filter_data=pd.read_sql_query(\"""SELECT * FROM emergency_calls\""",con)

# Thank you: Affanhamid
# https://medium.com/@affanhamid007/how-to-convert-csv-to-sql-database-using-python-and-sqlite3-b693d687c04a
"""

import sqlite3
import pandas as pd

# create the database
conn = sqlite3.connect('2025-02-13_emerg_data_organized_via_sqlite3.db') # Connecting to the database
cursor = conn.cursor() # Object to run queries

# create an SQLite table
df = pd.read_csv('2024-12-22_emerg_data_date_is_now_year_new_time_in_seconds_columns.csv')
df.info()

# add each of these columns to our query
table_name = 'emergency_calls'

create_table_with_types = '''CREATE TABLE IF NOT EXISTS emergency_calls( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_date TEXT NOT NULL,
    incident_date_year_only INTEGER NOT NULL,
    response_unit TEXT NOT NULL,
    call_type TEXT NOT NULL,
    dispatch_time TEXT NOT NULL,
    dispatch_time_in_seconds INTEGER NOT NULL,
    enroute_time TEXT NOT NULL,
    enroute_time_in_seconds INTEGER NOT NULL,
    arrive_time TEXT NOT NULL,
    arrive_time_in_seconds INTEGER NOT NULL,
    time_in_service TEXT NOT NULL,
    time_in_service_in_seconds INTEGER NOT NULL);
    '''


# Or something like this:
# create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types});"

cursor.executescript(create_table_with_types)
cursor.fetchall()

# run the command to check if table has been created
cursor.execute('pragma table_info(emergency_calls);')
cursor.fetchall()

# If everything has gone well so far,
# Load the data
for index, row in df.iterrows():
    values = ", ".join([f'"{row_item}"' for row_item in row])
    insert_sql = f"INSERT INTO {table_name} ({', '.join(df.columns.str.replace(' ', '_'))}) VALUES ({values})"
    cursor.execute(insert_sql)

# check the number of rows in the dataframe
# and in the sqlite table
df.shape # Returns number of records

cursor.execute('SELECT COUNT(*) FROM emergency_calls')
cursor.fetchall() # Returns [(6896,)]

# commit activity to the connection and close it.
conn.commit()

# After finishing all your SQL queries, close the connection.
conn.close()

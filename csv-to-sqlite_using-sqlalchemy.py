import csv

# Here is one way from: Emily Rosemary Collins at
# https://blog.finxter.com/5-best-ways-to-convert-csv-to-sqlite-in-python/
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

# Create a SQLite engine
engine = create_engine('sqlite:///2024-12-11_emerg_data_organized_via_sqlalchemy.db')

# Read the CSV file into a DataFrame
df = pd.read_csv('2024-12-11_emerg_data_organized.csv')

# Write the data to a SQLite table
df.to_sql('emergency_calls', con=engine, if_exists='replace', index=False)

# check the number of rows in the dataframe
# and in the sqlite table
df.shape # Returns the number of records

# References: 
# https://docs.sqlalchemy.org/en/20/core/connections.html#streaming-with-a-dynamically-growing-buffer-using-stream-results
# https://docs.sqlalchemy.org/en/20/core/connections.html#using-server-side-cursors-a-k-a-stream-results
# Then do something like this to verify:
with engine.connect() as conn:
    with conn.execution_options(stream_results=True, max_row_buffer=100).execute(
        text("SELECT COUNT(*) FROM emergency_calls")
    ) as result:
        for row in result:
            print(f"{row}")

# commit to the connection 
conn.commit() # commits "some statement"

# and when completely finished, close it.
conn.close()

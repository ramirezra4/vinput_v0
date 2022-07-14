from multiprocessing import connection
import pyodbc as dbc
import pandas as pd


"""Test Attributes"""
# used to connect to local db
# spec connection string for accessing server
DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'CULA-F6W7Z23'
DATABASE_NAME = 'vinput'

# connection string
connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""
# connection object
conn = dbc.connect(connection_string)

# cursor object instantiates interface between Python and DB
cursor = conn.cursor()

# query passed to cursor
query = "SELECT VIN, MileageBand, Month24, Month30, Month36 FROM [dbo].[Used Leasing DB JA22 CULA VIN Specific File] WHERE VIN = '1GYS4HKJXHR376823'"

# execute query by cursor
cursor.execute(query)

# grab data from cursor
data = cursor.fetchall()

# create dataframe to parse data
df = pd.DataFrame(data)


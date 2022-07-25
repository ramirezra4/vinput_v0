from dataclasses import dataclass
import pyodbc as dbc
import pandas as pd
from sympy import ilcm
from MMRcall import MMRapi


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


def query_vin(i):
    """
    Primary means of accessing the CULA RV database. Tries to map
    VIN's to RV's directly in CULA database. 
    """
    query = f"""
    SELECT VIN, 
    NADA_VehicleID, 
    MileageBand, 
    Month24, 
    Month30, 
    Month36, 
    Month39, 
    Month42, 
    Month48, 
    Month60 
    FROM [dbo].[Used Leasing DB JA22 CULA VIN Specific File] WHERE VIN = '{i}'
    """
    cursor.execute(query)
    data = cursor.fetchall()
    data = to_df(data)

    return data


def to_df(data):
    lst = []
    for i in data:
        for j in i:
            lst.append(j)
    df = pd.DataFrame(lst)
    df_t = df.transpose()
    return df_t







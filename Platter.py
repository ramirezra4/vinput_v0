from pickle import TRUE
import pypyodbc as dbc
import pandas as pd

from Cnx import Cnx

class Platter:

    # instantiate server connection object
    cnx = Cnx()

    _df = ''

    def __init__(self, vin, term):
        self.vin = vin
        self.term = term

    def hit_cula(self):
        "Checks for VIN -> RV mapping internally."
        self.query()
        if self._df.size == 2:
            # HIT MMR. FIXME
            print("HITTING MMR")
        else:
            # SERVE UP RV's FIXME
            print(self._df)
        
    def query(self):
        self.cnx._query = f"""
            SELECT VIN, MileageBand, Month24, Month30, Month36 
            FROM [dbo].[Used Leasing DB JA22 CULA VIN Specific File]
            WHERE VIN = '{self.vin}'
        """
        self.cnx._cursor.execute(self.cnx._query)
        self.cnx._data = self.cnx._cursor.fetchall()
        self._df = self.cnx.to_df()

Platter('1GYS4HKJXHR376823').hit_cula()
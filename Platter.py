import pypyodbc as dbc
import pandas as pd
import MMRcall
from Cnx import Cnx

class Platter:
    """
    **UNSECURE**

    Platter takes in VIN numbers and serves up a piping hot
    set of residual values.

    In implementing this app I made a couple of important assumptions
    about the peripheral systems involved, namely:

    1. Company server and authentication therein is static.
    2. MMR API authentication key is static.
    3. All information handled is unsecured.

    With those two assumptions I have decided that the configuration for connecting
    to these outside components should be hardcoded. OOP features will abstract logic
    encapsulating authentication so as to allow for future security augmentations to
    be made relatively painlessly.

    Below will be an abstract implementation of the app in general to guide development
    and view at a high level the chain of logic connecting each of the many dependent sources
    to each other to achieve the desired output.
    """

    cnx = Cnx()
    "Instantiate server connection object and dataframe for queries"
    
    _df_column_names = []
    _df = ''

    
    mmr = ''
    "Create Request object for MMR API Call"

    mmrmap = {}
    "Dictionary containing body:nada vehicle id mappings"

    nada_lst = []


    def __init__(self, vin, term='Month36'):
        self.vin = vin
        self.term = term
        self._df_column_names = ['VIN', f'Term: {self.term}']

    def hit_cula(self, mmr=True):
        "Checks for VIN -> RV mapping internally."
        self.query_vin()
        if self._df.empty:
            # HIT MMR. FIXME
            print("HITTING MMR")
            self.mmr = MMRcall.MMRapi(self.vin)
            temp_dict = self.mmr.match()
            
            # iterate through the temp dict to extract useful pairs
            for model in temp_dict:
                self.mmrmap.update({model['body']: model['ucgvehicleid']})
            
            # iterate through useful pairs to prepare query
            for vid in self.mmrmap:
                self.nada_lst.append(model['ucgvehicleid'])

            # query database to extract RV's
            for nada in self.nada_lst:
                self.query_nada(nada)
                print(self._df)


        else:
            # SERVE UP RV's FIXME
            print(self._df)
    
    def query_vin(self):
        "QUERY_VIN queries RV's on a given term from CULA internal database."
        self.cnx._query = f"""
            SELECT VIN, {self.term} 
            FROM [dbo].[Used Leasing DB JA22 CULA VIN Specific File]
            WHERE VIN = '{self.vin}'
        """
        self.cnx._cursor.execute(self.cnx._query)
        self.cnx._data = self.cnx._cursor.fetchall()
        self._df = self.cnx.to_df()
        self._df.columns = self._df_column_names

    def query_nada(self, nada):
        "QUERY_NADA queries RV's on a given term from CULA internal database."
        self.cnx._query = f"""
            SELECT VIN, NADA_VehicleID, {self.term} 
            FROM [dbo].[Used Leasing DB JA22 CULA VIN Specific File]
            WHERE VIN = '{self.vin}' AND NADA_VehicleID = '{nada}'
        """
        self.cnx._cursor.execute(self.cnx._query)
        self.cnx._data = self.cnx._cursor.fetchall()
        self._df = self.cnx.to_df()
        self._df.columns = self._df_column_names = ['']

# print test cases will have to do for now
Platter('1GYS4HKJXHR376823').hit_cula()
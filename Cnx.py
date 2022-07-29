import pypyodbc as dbc
import pandas as pd

class Cnx:
    """
    **SECURE**
    Interface with CULA Internal Databases.
    """
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
    _conn = dbc.connect(connection_string)

    # cursor object instantiates interface between Python and DB
    _cursor = _conn.cursor()

    # grab data from cursor
    _data = ''

    def __init__(self, driver='', server='', database='', query= ''):
        if driver == '' and server == '' and database == '' or query == '':
            pass
        else:
            self.DRIVER_NAME = driver
            self.SERVER_NAME = server
            self.DATABASE_NAME = database
            self.query = query

    def set_query(self, q):
        """Set the query."""
        self.query = q

    def execute(self):
        """
        Execute Query --> (_query).
        Returns resulting data.
        """
        self._cursor.execute(self.query)
        return self._cursor.fetchall() 

    
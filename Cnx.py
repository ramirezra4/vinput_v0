import pypyodbc as dbc

class Cnx:
    """
    **SECURE**
    Interface with CULA Internal Databases.
    For production purposes, update DRIVER_NAME,
    SERVER_NAME, AND DATABASE_NAME attributes to
    production counterparts.
    """
    # spec connection string for accessing server
    # currently configured to connect to local db, change me for production.
    DRIVER_NAME = 'SQL SERVER'
    SERVER_NAME = 'CULA-F6W7Z23'
    DATABASE_NAME = 'vinput'
    TABLE = 'ALGResidualNewTable20220708'

    ## WARNING!!!
    ## Do not reconfigure anything below.
    ## (as it is not necessary and will break things.)

    # connection string
    connection_string = f"""
        DRIVER={{{DRIVER_NAME}}};
        SERVER={SERVER_NAME};
        DATABASE={DATABASE_NAME};
        Trust_Connection=yes;
    """
    
    # connection object (refer to Pyobdc for more info on what that is)
    _conn = dbc.connect(connection_string)

    # cursor object instantiates interface between Python and SQL database
    _cursor = _conn.cursor()

    # data from cursor
    _data = ''

    def __init__(self, driver='', server='', database='', query= ''):
        """
        Initialize a CNX class. Instantiates a connection object through which
        I can interact with SQL databases.
        """
        if driver == '' and server == '' and database == '' or query == '':
            pass
        else:
            self.DRIVER_NAME = driver
            self.SERVER_NAME = server
            self.DATABASE_NAME = database
            self.query = query

    def set_query(self, q):
        """
        Stage a query for this connection object.
        Returns None.
        """
        self.query = q

    def execute(self):
        """
        Execute previously set query --> (_query).
        Returns resulting data.
        """
        self._cursor.execute(self.query)
        return self._cursor.fetchall() 

    
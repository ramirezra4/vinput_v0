import pypyodbc as dbc
import pandas as pd
import MMRcall
from Cnx import Cnx
import sql_query

"""
Platterfunc takes in a batch of VIN numbers and serves up
a piping hot set of residual values.
"""

# STATIC VARS
# ...

mmr = MMRcall
"MMR API Interface Object"

def main(vins):
    """
    Input: [vin_1, vin_2,...,vin_n]
    Output: Dataframe of residuals with axes: (Term, MileageBand)
    """
    
    temp_dataframe = []
    
    for v in vins:    
        temp_dataframe.append(sql_query.query_vin(v))
    
    rv_dataframe = pd.concat(temp_dataframe)
    return rv_dataframe




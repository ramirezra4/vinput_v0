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
    
    # FIXME
    # hit cula, flag = 'VIN'
        # return RV's else flag = 'NADA_VehicleID' 
        # hit mmr -^
            # hit cula (hit mmr)
            # return rv's
    residuals = query_cula(vins)
    df_rv = pd.DataFrame(residuals) 
 
    return df_rv

def query_cula(vins):
    try:
        out = [] # empty array
        for vin in vins: # iterate over batch of vins
            out += sql_query.query_vin(vin) # append the result of the sql query to out. VP: VIN^1 --> NADA^n
        return out
        
    except:
        return("Query Failed.")

df = query_cula(['5UXKR0C59JL071122', 'LRBFX2SA0JD026226', '1GYKNDRS3JZ132358'])
print(df)


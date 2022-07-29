import pypyodbc as dbc
import pandas as pd
from MMRcall import MMRapi
from Cnx import Cnx
import query as query
import make as mk
from fuzzywuzzy import fuzz

"""
Platterfunc takes in a batch of VIN numbers and serves up
a piping hot set of residual values.
"""

# STATIC VARS
# ...

"MMR API Interface Object"

def main_test(vin):
    """
    Input: VIN.
    Output: Dict of residuals with axes: 
    {Make, Model, Trim, Term_1,..., Term_n, MileageBand_1,..., MileageBand_n}
    """
    conn = Cnx()
    mmr = MMRapi(vin)
    """Access MMR Api"""
    slice_bymake = f"""
    SELECT [ALGResidualNewID]
    ,[ModelYear]
    ,[MakeNumber]
    ,[ModelNumber]
    ,[Style]
    ,[ModelDesc]
    ,[Description]
    ,[Month24]
    ,[Month30]
    ,[Month36]
    ,[Month42]
    ,[Month48]
    ,[Month54]
    ,[Month60]
    FROM [vinput].[dbo].[ALGResidualNewTable20220708]
    WHERE MakeNumber = {mk.make_number[mmr.make()][0]} AND
    ModelYear = {mmr.model_year()}
    """
    conn.set_query(slice_bymake)
    make_match = conn.execute()
    make_df = pd.DataFrame(make_match)
    print(make_df.head())

def main(vin):
    """
    Input: VIN.
    Output: Dict of residuals with axes: 
    {Make, Model, Trim, Term_1,..., Term_n, MileageBand_1,..., MileageBand_n}
    """
    conn = Cnx()
    mmr = MMRapi(vin)
    make = mmr.make()
    bod = mmr.body()
    """Access MMR Api"""
    slice_bymake = f"""
    SELECT [ALGResidualNewID]
    ,[ModelYear]
    ,[MakeNumber]
    ,[ModelNumber]
    ,[Style]
    ,[ModelDesc]
    ,[Description]
    ,[Month24]
    ,[Month30]
    ,[Month36]
    ,[Month42]
    ,[Month48]
    ,[Month54]
    ,[Month60]
    FROM [vinput].[dbo].[ALGResidualNewTable20220708]
    WHERE MakeNumber = {mk.make_number[make]} AND
    ModelYear = {mmr.model_year()}
    """
    conn.set_query(slice_bymake)
    make_match = pd.DataFrame(conn.execute())
    make_df = make_match
    make_df.columns = [
        'ALGResidualNewID',
        'ModelYear',
        'MakeNumber',
        'ModelNumber',
        'Style',
        'ModelDesc',
        'Description',
        'Month24',
        'Month30',
        'Month36',
        'Month42',
        'Month48',
        'Month54',
        'Month60'
        ]
    match_index = -1
    match_max = -1
    make_df['Fuzzy'] = make_df['Description']
    for i in range(make_df['Fuzzy'].size):
        make_df['Fuzzy'][i] = fuzz.partial_ratio(make_df['Fuzzy'][i], bod)
        if make_df['Fuzzy'][i] > match_max:
            match_index = i
            match_max = make_df['Fuzzy'][i]
    
    return make_df.iloc[match_index]

    
def to_df(data):
    lst = []
    for i in data:
        for j in i:
            lst.append(j)
    df = pd.DataFrame(lst)
    df_t = df.transpose()
    return df_t

jeepers = main('19UDE2F76NA004740')
print(jeepers)
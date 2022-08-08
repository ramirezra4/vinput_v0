import vinwhiz as wiz
import pandas as pd
from Cnx import Cnx

def slice(i, end, start=0):
    """
    Helper function for string manipulation.
    Takes in an object I and returns a string,
    sliced from index in I from start (default=0)
    to end.
    """
    return str(i)[start:end]

def main(vin, region):
    """
    Main functional interface for VINPUT.
    Input: VIN Number, State (abr).
    Output: Dataframe
    """
    algcode = wiz.vin_alg(vin)
    make_number = slice(algcode, 3)
    model_num = slice(algcode, 6, 3)
    style_num = slice(algcode, 9, 6)
    model_year = wiz.vin_year(vin)
    conn = Cnx()
    quer = f"""
        SELECT 
        [ModelYear],
        [Description], 
        [MakeNumber],
        [ModelNumber],
        [Style],
        [Region],
        [EffectiveDate]
        FROM [vinput].[dbo].[ALGResidualNewTable20220708]
        WHERE [MakeNumber] = {make_number} AND
        [ModelNumber] = {model_num} AND
        [Style] = {style_num} AND
        [ModelYear] = {model_year} AND
        [Region] = '{region}'
    """
    conn.set_query(quer)
    make_match = conn.execute()
    df = pd.DataFrame(make_match)
    df.columns = ['Model Year', 'Description', 'Make Number', 'Model Number', 'Style', 'Region', 'Effective Date']
    df = df[df['Effective Date'] == df['Effective Date'].max()]
    return df.to_json()
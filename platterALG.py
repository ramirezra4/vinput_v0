from MMRcall import MMRapi
import vinwhiz as wiz
import pandas as pd
from Cnx import Cnx
from dateutil import parser

def slice(i, end, start=0):
    """
    Helper function for string manipulation.
    Takes in an object I and returns a string,
    sliced from index in I from start (default=0)
    to end.
    """
    return str(i)[start:end]

def main(vin, region, date):
    """
    Main functional interface for VINPUT.
    Input: VIN Number, State (abr).
    Output: Dataframe
    """
    # fix date format for internal use
    date = parser.parse(date)
    # Create Vehicle Descriptions Dict
    mmr = MMRapi(vin)
    mmr.match()
    mmr_make = mmr.make()
    mmr_model = mmr.model()
    mmr_style = mmr.body()
    mmr_yr = mmr.model_year()
    vehicle_desc = {
        'Make': mmr_make,
        'Model': mmr_model,
        'Style': mmr_style
    }

    algcode = wiz.vin_alg(vin)
    make_number = slice(algcode, 3)
    model_num = slice(algcode, 6, 3)
    style_num = slice(algcode, 9, 6)
    model_year = wiz.vin_year(vin)
    conn = Cnx()
    quer = f"""
        SELECT 
        [ModelYear], 
        [MakeNumber],
        [ModelNumber],
        [Style],
        [Month24],
        [Month30],
        [Month36],
        [Month42],
        [Month48],
        [Month54],
        [Month60],
        [MRM],
        [EffectiveDate],
        [Region]
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
    df.columns = [
        'Model Year',
        'Make Code',
        'Model Code',
        'Style Code',
        'Month 24',
        'Month 30',
        'Month 36',
        'Month 42',
        'Month 48',
        'Month 54',
        'Month 60',
        'MRM',
        'Effective Date',
        'Region'
    ]
    
    dtmdt = lambda y: parser.parse(y)
    df['Effective Date'] = df['Effective Date'].apply(dtmdt)
    df = df.drop(df[df['Effective Date'] > date].index)
    df = df[df['Effective Date'] == df['Effective Date'].max()]
    return df.iloc[0].to_dict()
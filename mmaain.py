import requests
import pandas as pd
from Cnx import Cnx

def get_styleID(vin):
    url = f'https://apitesting.vinwhiz.com/api/v1.1/vins/{vin}/ris'
    api_key = '2D979E71-EE01-4B7D-A995-F2A2D29A5E85'
    r = requests.get(url, headers={"x-apikey": f"{api_key}", "accept": "application/json"})
    #print(r.json()['signals'][0]['styleId'])
    return r.json()['signals'][0]['styleId']

def vin_year(vin):
    url = f'https://apitesting.vinwhiz.com/api/v1.1/vins/{vin}/ris'
    api_key = '2D979E71-EE01-4B7D-A995-F2A2D29A5E85'
    r = requests.get(url, headers={"x-apikey": f"{api_key}", "accept": "application/json"})
    return r.json()['signals'][0]['vehicleHints']['YEAR']

# print(get_styleID('5UXCR6C09N9M97942'))

def style_to_ALGcode(styleId):
    chrmap = pd.read_csv('ALG_US_CHROMEMAP.csv')
    chrmap = chrmap[chrmap.ChromeStyleId == styleId]
    return chrmap['AlgCode'].iloc[0] 

def vin_alg(vin):
    return style_to_ALGcode(get_styleID(vin))

def slice(i, end, start=0):
    return str(i)[start:end]

def main(vin):
    """
    Main functional interface for VINPUT.
    Input: VIN Number.
    Output: Dataframe
    """
    algcode = vin_alg(vin)
    make_number = slice(algcode, 3)
    model_num = slice(algcode, 6, 3)
    style_num = slice(algcode, 9, 6)
    model_year = vin_year(vin)
    conn = Cnx()
    quer = f"""
        SELECT 
        [ModelYear],
        [Description], 
        [MakeNumber],
        [ModelNumber],
        [Style],
        [Month24],
        [Month30],
        [Month36],
        [Month42],
        [Month48],
        [Month54],
        [Month60]
        FROM [vinput].[dbo].[ALGResidualNewTable20220708]
        WHERE [MakeNumber] = {make_number} AND
        [ModelNumber] = {model_num} AND
        [Style] = {style_num} AND
        [ModelYear] = {model_year}
    """
    conn.set_query(quer)
    make_match = conn.execute()
    df = pd.DataFrame(make_match)
    return df

print(main('5UXCR6C09N9M97942'))
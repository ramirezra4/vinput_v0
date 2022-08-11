import requests
import pandas as pd 

_api_key = '2D979E71-EE01-4B7D-A995-F2A2D29A5E85'

def _url(vin):
    return  f'https://apitesting.vinwhiz.com/api/v1.1/vins/{vin}/ris'

def get_nummaps(vin):
    r = requests.get(_url(vin), headers={"x-apikey": f"{_api_key}", "accept": "application/json"})
    return len(r.json()['signals'])

def get_styleID(vin, i=0):
    r = requests.get(_url(vin), headers={"x-apikey": f"{_api_key}", "accept": "application/json"})
    return r.json()['styleIds'][i]

def get_styleIDs(vin):
    r = requests.get(_url(vin), headers={"x-apikey": f"{_api_key}", "accept": "application/json"})
    return r.json()['styleIds']

def vin_year(vin):
    r = requests.get(_url(vin), headers={"x-apikey": f"{_api_key}", "accept": "application/json"})
    return r.json()['signals'][0]['vehicleHints']['YEAR']

def style_trims(vin):
    r = requests.get(_url(vin), headers={"x-apikey": f"{_api_key}", "accept": "application/json"})
    trim_dict = {}
    for signal in r.json()['signals']:
        trim_dict.update({signal['styleId']: (f"{signal['vehicleHints']['BODY_TYPE']} {signal['vehicleHints']['TRIM']} {signal['vehicleHints']['ENGINE_CODE']} {signal['vehicleHints']['DRIVE_TYPE_CODE']}")})
    return trim_dict

def style_to_ALGcode(styleId):
    chrmap = pd.read_csv('ALG_US_CHROMEMAP.csv')
    chrmap = chrmap[chrmap.ChromeStyleId == styleId]
    return chrmap['AlgCode'].iloc[0] 

def ALGcode_to_style(algcode):
    chrmap = pd.read_csv('ALG_US_CHROMEMAP.csv')
    chrmap = chrmap[chrmap.AlgCode == algcode]
    return chrmap['ChromeStyleId'].iloc[0] 

def vin_alg(vin):
    return style_to_ALGcode(get_styleID(vin))

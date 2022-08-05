import requests
import pandas as pd 

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
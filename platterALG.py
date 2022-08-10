import json
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

def adjustment(df, term, ann_miles, inception_miles):
    """
    Adjusts residual values based on:
    Term, Annual Mileage, MSRP, and Inception Miles.
    Takes in a pandas dataframe and the above parameters.
    Returns a dataframe containing adjusted RV's.

    Equations:
    RV$ calculation = (RV% * minimum (MSRP or MRM)) + inception mileage adjustment)
    """
    terms = {
        24: 'Month 24',
        30: 'Month 30',
        36: 'Month 36',
        42: 'Month 42',
        48: 'Month 48',
        54: 'Month 54',
        60: 'Month 60',
    }
    if inception_miles < 500:
        inception_adj = 0
    else:
        inception_adj = (inception_miles - 500) * -0.15
    if ann_miles > 15000:
        term_adj = ((ann_miles * term) - (15000 * term)) * -0.15
    else:
        term_adj = 0
    rv_perc = ((df[terms[term]] * 0.001)) + term_adj
    rv_perc_inc = ((df[terms[term]] * 0.001)) + term_adj + inception_adj
    return {"RV Perc": rv_perc, "RV Perc Inception": rv_perc_inc, "Term": terms[term]}



def main(vin, region, date, term, ann_miles, msrp, inception_miles):
    """
    Main functional interface for VINPUT.
    Input: VIN Number, State (abr).
    Output: Dataframe
    """
    # parse user inputted date
    date = parser.parse(date)
    
    # grab mmr vehicle descriptions
    mmr = MMRapi(vin)
    mmr.match()
    mmr_make = mmr.make()
    mmr_model = mmr.model()
    mmr_style = mmr.body()

    # grab 
    algcode = wiz.vin_alg(vin)
    make_number = slice(algcode, 3)
    model_num = slice(algcode, 6, 3)
    style_num = slice(algcode, 9, 6)
    model_year = wiz.vin_year(vin)

    # create query object to interface with CULA servers
    conn = Cnx()

    # build query string
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
    
    # get min(mrm, msrp)
    if df['MRM'] < msrp:
        df['MRM'] = msrp

    dtmdt = lambda y: parser.parse(y)
    df['Effective Date'] = df['Effective Date'].apply(dtmdt)
    df = df.drop(df[df['Effective Date'] > date].index)
    df = df[df['Effective Date'] == df['Effective Date'].max()]
    df.pop('Region')
    df = df.iloc[0]

    if term:
        ret = adjustment(df, term, ann_miles, msrp, inception_miles)
        out_dict = {
           'Model Year': str(df['Model Year']),
           'Vehicle Descriptions': {
                'Make': str(mmr_make),
                'Model': str(mmr_model),
                'Style': str(mmr_style)
           },
            'ALG Codes': {
                'Make': str(df['Make Code']),
                'Model': str(df['Model Code']),
                'Style': str(df['Style Code']),
            },
            'Term': ret['Term'],
            'Residuals': {
                'RV Percentage': str(ret['RV Perc']),
                'Adjusted': str(ret['RV Perc Inception'] * df['MRM'])
            },
            'MRM': df['MRM'],
            'Effective From': df['Effective Date']
        }

    else:
        out_dict = {
            'Model Year': str(df['Model Year']),
            'Vehicle Descriptions': {
                'Make': str(mmr_make),
                'Model': str(mmr_model),
                'Style': str(mmr_style)
            },
            'ALG Codes': {
                'Make': str(df['Make Code']),
                'Model': str(df['Model Code']),
                'Style': str(df['Style Code'])
            },
            "RV's 15k": {
                'Month 24': str(df['Month 24']),
                'Month 30': str(df['Month 30']),
                'Month 36': str(df['Month 36']),
                'Month 42': str(df['Month 42']),
                'Month 48': str(df['Month 48']),
                'Month 54': str(df['Month 54']),
                'Month 60': str(df['Month 60']),
            },
            'MRM': str(df['MRM']),
            'Effective Date': str(df['Effective Date'])
            
        }
    return out_dict
    
    
print(main('WP0AA2A92NS205471', 'S', '2022-03-06'))


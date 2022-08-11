import json
from NADAcall import MMRapi
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

def adjustment(df, term, ann_miles, msrp, inception_miles):
    """
    Adjusts residual values based on:
    Term, Annual Mileage, MSRP, and Inception Miles.
    Takes in a pandas dataframe and the above parameters.
    Returns a dataframe containing adjusted RV's.

    Equations:
    RV$ calculation = (RV% * minimum (MSRP or MRM)) + inception mileage adjustment)
    """
    msrp = min(df['MRM'], msrp)
    # convert strings to ints
    term, ann_miles, inception_miles = int(term), int(ann_miles), int(inception_miles)
    terms = {
        24: 'Month 24',
        30: 'Month 30',
        36: 'Month 36',
        42: 'Month 42',
        48: 'Month 48',
        54: 'Month 54',
        60: 'Month 60',
    }

    # calculate raw residual before processing
    rv_dollar = df[terms[term]] * 0.001 * msrp
    rv_perc = df[terms[term]]

    if inception_miles < 500:
        inception_adj = 0
        inception_adj_perc = 0
    else:
        inception_adj = (inception_miles - 500) * -0.15
        inception_adj_perc = (inception_adj) * 0.001

    if ann_miles > 15000:
        term_adjustment = (-0.15 * ((ann_miles * term/12) - (15000 * term/12)))
        term_adjustment_perc = term_adjustment * 0.001
    else:
        term_adjustment = 0
        term_adjustment_perc = 0

    adjustment = term_adjustment + inception_adj
    adjustment_perc = term_adjustment_perc + inception_adj_perc

    rv_perc = rv_perc + adjustment_perc
    rv_real = (rv_dollar + adjustment) * 10
    return {"RV Perc": rv_perc, "RV Adjusted": rv_real, "Term": terms[term]}

def main(vin, region, date, algcode='', term='', ann_miles='', msrp='', inception_miles=''):
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

    # grab all the vinwhiz stuff
    #algcode = wiz.vin_alg(vin)
    make_number = slice(algcode, 3)
    model_num = slice(algcode, 6, 3)
    style_num = slice(algcode, 9, 6)
    model_year = wiz.vin_year(vin)
    chrom_style_id = wiz.ALGcode_to_style(algcode)
    descriptions = wiz.style_trims(vin)


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

    dtmdt = lambda y: parser.parse(y)
    df['Effective Date'] = df['Effective Date'].apply(dtmdt)
    df = df.drop(df[df['Effective Date'] > date].index)
    df = df[df['Effective Date'] == df['Effective Date'].max()]
    df.pop('Region')
    df = df.iloc[0]
    
    # Grab correct vehicle description
    descriptionss = descriptions[chrom_style_id]
    if term:
        ret = adjustment(df, term, ann_miles, msrp, inception_miles)
        out_dict = {
           'Model Year': str(df['Model Year']),
           'Vehicle Descriptions': {
                'Make': str(mmr_make),
                'Model': str(mmr_model),
                'Style': descriptionss
           },
            'ALG Codes': {
                'Make': str(df['Make Code']),
                'Model': str(df['Model Code']),
                'Style': str(df['Style Code']),
            },
            'Term': ret['Term'],
            'Residuals': {
                'RV%': str(ret['RV Perc']),
                'Residual Value': str(ret['RV Adjusted'])
            },
            'MRM': df['MRM'],
            'Effective From': slice(str(df['Effective Date']), 10)
        }

    else:
        out_dict = {
            'Model Year': str(df['Model Year']),
            'Vehicle Descriptions': {
                'Make': str(mmr_make),
                'Model': str(mmr_model),
                'Style': descriptionss
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
            'Effective Date': slice(str(df['Effective Date']), 10)
            
        }
    return out_dict


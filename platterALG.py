from flask import jsonify
import vinwhiz as wiz
import pandas as pd
from Cnx import Cnx
from platterfunc import main as m

def main(vin):
    try:
        algcode = wiz.vin_alg(vin)
        conn = Cnx()
        quer = f"""
            SELECT
            [ModelYear],
            [Description], 
            [Region],
            [Month24],
            [Month30],
            [Month36],
            [Month42],
            [Month48],
            [Month54],
            [Month60] 
            FROM [vinput].[dbo].[ALGResidualNewTable20220708]
            WHERE ALGResidualNewID = f{algcode}
        """
        conn.set_query(quer)
        make_match = conn.execute()
        df = pd.DataFrame(make_match)
        return df
    except:
        return m(vin)
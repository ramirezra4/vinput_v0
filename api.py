from flask import Flask, jsonify
from platterALG import main
from state_to_region import state_region
from vinwhiz import vin_alg

"""
Web interface for vinput API.
"""

app = Flask(__name__)
"""Instantiate Flask Web App"""

@app.route('/algcode/vin=<string:vin>', methods=['GET'])
def get_algcode(vin):
    """
    Input: VIN
    Output: ALG code.
    """
    _algcode = str(vin_alg(vin))
    return jsonify({'ALG Code': _algcode, 'VIN': vin})

@app.route('/15kresiduals/vin=<string:vin>&state=<string:state>&date=<string:date>', methods=['GET'])
def get_vinmap(vin, state, date):
    """
    Input: Vin, State, Contract Date
    Output: Model Year, Vehicle Descriptions (Make, Model, Style), ALG Codes (Make Model Style), RVs 
    """
    return jsonify(main(vin, state_region[state], date))

@app.rorute('/singledeal/vin=<string:vin>&state=<string:state>&date=<string:date>&mileage_band=<string:mileage_band>&msrp=<string:msrp>&inception_miles=<string:inception_miles>')
def get_deal(df, term, ann_miles, msrp, inception_miles):
    out = main(df, term, ann_miles, msrp, inception_miles)
    return jsonify(out)

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0')
import json
from flask import Flask, jsonify
from platterALG import main
from state_to_region import state_region
from vinwhiz import style_to_ALGcode, vin_alg, get_nummaps, get_styleID, get_styleIDs

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
    if get_nummaps == 0:
        return "RV's for this vehicle are not yet available. (Update Chrome_Style_Mapping)"
    main_list = []
    for id in get_styleIDs(vin):
        code = style_to_ALGcode(id)
        main_list.append(main(vin, state_region[state], date, algcode=code))    

    return jsonify(main_list)

@app.route('/singledeal/vin=<string:vin>&state=<string:state>&date=<string:date>&term=<string:term>&mileage_band=<string:mileage_band>&msrp=<string:msrp>&inception_miles=<string:inception_miles>')
def get_deal(vin, state, date, term, mileage_band, msrp, inception_miles):
    if get_nummaps == 0:
        return "RV's for this vehicle are not yet available. (Update Chrome_Style_Mapping)"
    term = int(term)
    mileage_band = int(mileage_band)
    msrp = int(msrp)
    inception_miles = int(inception_miles)
    main_list = []
    for id in get_styleIDs(vin):
        code = style_to_ALGcode(id)
        main_list.append(main(vin, state_region[state], date, code, term, mileage_band, msrp, inception_miles))    

    return jsonify(main_list)

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0')
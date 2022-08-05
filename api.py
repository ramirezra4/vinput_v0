from flask import Flask, jsonify
from platterALG import main

"""
Web interface for vinput API.
"""

app = Flask(__name__)
"""Instantiate Flask Web App"""

@app.route('/vinput/vin=<string:vin>', methods=['GET'])
def get_vinmap(vin):
    """Create """
    return jsonify(main(vin).to_dict())

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0')
from multiprocessing.connection import wait
from flask import Flask, jsonify
from platterALG import main

app = Flask(__name__)

@app.route("/test")
def hello():
    return jsonify({"Hello": "Hello World!"})

@app.route('/vinput/vin=<string:vin>', methods=['GET'])
def get_vinmap(vin):
    return jsonify(main(vin).to_dict())

@app.route('/multi/num=<int:num>', methods=['GET'])
def get_multiply(num):
    return jsonify({'result': num*10})

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0')
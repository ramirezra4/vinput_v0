from flask import Flask
from flask_restful import Resource, Api, reqparse
from platterfunc import main

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('vin')

class Welcome(Resource):
    def get(self):
        return {
            'Welcome to': 'vinput',
            'Enter a vin via': '/vinput'
            }

class VinPut(Resource):
    def get(self, vin):
        args = parser.parse_args()
        vin = {'vin': args['vin']}
        return main(vin).to_json()


##
## Api resource routing below
##
api.add_resource(Welcome, '/')
api.add_resource(VinPut, '/vinput')

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0')
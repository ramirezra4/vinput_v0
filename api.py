from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Platter(Resource):
    def get(self):
        return {'Residuals': 'Served'}

api.add_resource(Platter, '/')

if __name__ == '__main__':
    app.run(debug=True)
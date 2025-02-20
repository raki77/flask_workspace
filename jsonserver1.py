from flask import Flask
from flask_restful import Resource, Api

from flask import request
from flask import session
from flask import render_template

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello':'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)

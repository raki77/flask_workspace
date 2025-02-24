from flask import Flask
from flask_restful import Resource, Api

from flask import request
from flask import session
from flask import render_template

app = Flask(__name__)
# api 와 app 연동 작업
api = Api(app)

# Resource 클래스를 상속 받는다.
class HelloWorld(Resource):
    # post, put, delete 이미 정해져 있다. get
    def get(self):
        # dict -> json 객체로 출력한다.
        return {'hello':'world'}

# url과 자원을 연결 한다.
api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {'1':'go to company', '2': 'go to movie'}

# http://127.0.0.1:5000/1
class TodoSimple(Resource):
    
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}
    
    def post(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
    
    
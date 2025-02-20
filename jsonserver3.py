from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
# CORS 에러처리
from flask_cors import CORS, cross_origin


app = Flask(__name__)
api = Api(app)

#CORS(app, resources={r'*':{'origins':'https://webisfree.com'}})


TODOS = {
    'todo1': {'task':'build an API'},
    'todo2': {'task':'play'},
    'todo3': {'task':'profit!'}
}

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

# 클라이언트로부터 오는 값을 리스트에 저장하기 위한 파서 선언하기
parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo #객체 하나만 보내기
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]
    # delete
    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204
    # put
    def put(self, todo_id): 
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201
    
# TodoList
class TodoList(Resource):
    def get(self):
        return TODOS
    def post(self):
        # 값 받아서 리스트에 추가한다.
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201
    
# 2 개의 리소스를 추가한다.
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
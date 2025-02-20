from flask import Flask, request, Response, Blueprint
from flask_restful import Resource, Api, reqparse
import json
from . import DBModule

# pip install flask_restful
app = Blueprint('guestbook', __name__)
# restful api 객체를 생성한다. 매개변수로 Flask 객체를 전달해야 한다.
api = Api(app)

db = DBModule.Database()
parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('title')
parser.add_argument('contents')
parser.add_argument('writer')

class Guestbook(Resource):
    def get(self, id=None):
        if id is None:
            sql = """
                select id, title, contents, writer,
                date_format(wdate, '%%y-%%m-%%d') wdate
                from guestbook
            """
            guestbookData = db.executeAll(sql)
            jsonStr = json.dumps(guestbookData, ensure_ascii=False).encode('utf8')
            return Response(jsonStr, content_type="application/json;charset=utf-8")
        else :
            sql = """
                select id, title, contents, writer,
                date_format(wdate, '%%y-%%m-%%d') wdate
                from guestbook where id=%s
            """
            guestbookData = db.executeOne(sql, (id,))
            jsonStr = json.dumps(guestbookData, ensure_ascii=False).encode('utf8')
            return Response(jsonStr, content_type="application/json;charset=utf-8")
    
    def post(self):
        args = parser.parse_args()
        sql = """
            insert into guestbook(title, contents, writer, wdate)
            values(%s, %s, %s, now())
        """
        db.execute(sql, (args['title'], 
                         args['contents'], 
                         args['writer']))
        return {"result":"200ok"}
    
    def put(self):
        args = parser.parse_args()
        sql = """
            update guestbook set title=%s, contents=%s, writer=%s
            where id=%s
        """
        db.execute(sql, (args['title'], args['contents'], args['writer'], args['id']))
        return {"result" : "200ok"}
    
    def delete(self, id=None):
        args = parser.parse_args()
        print("id=", id)
        sql = """
            delete from guestbook where id=%s
        """
        db.execute(sql, (id))
        return {"result": "200ok"}
    
api.add_resource(Guestbook, '/guestbook/list',
                            '/guestbook/view/<int:id>',
                            '/guestbook',
                            '/guestbook/<int:id>')

if __name__ == '__main__':
    pass
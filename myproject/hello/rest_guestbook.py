from flask import Flask, request, Response, Blueprint
from flask_restful import Resource, Api, reqparse
import json
from . import DBModule
# from DBModule import Database

# pip install flask_restful
app = Blueprint('rest_guestbook', __name__)
# restful api 객체를 생성한다. 매개변수로 Flask 객체를 전달해야 한다.
api = Api(app)
db = DBModule.Database()
# db = Database()

# form 태그로 전송받는 키값을 정리작업함.
parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('title')
parser.add_argument('contents')
parser.add_argument('writer')

# 플라스크의 모든 RestAPI는 Resource 상속 받아야 한다.
class Guestbook(Resource):
    # 2가지 목적. 목록화면, 상세화면
    # http://127.0.0.1:5000/rest_guestbook 목록
    # http://127.0.0.1:5000/rest_guestbook/1 상세화면
    def get(self, id=None):
        sql = """
            select id, title, contents, writer,
            date_format(wdate, '%%y-%%m-%%d') wdate
            from guestbook
        """            
        if id is None: 
            guestbookData = db.executeAll(sql)
            # 한글 수정
            jsonStr = json.dumps(guestbookData, ensure_ascii=False).encode('utf8')
            return Response(jsonStr, content_type="application/json;charset=utf-8")
        else :
            sql2 = sql + """ where id=%s"""
            guestbookData = db.executeOne(sql2, (id,))
            jsonStr = json.dumps(guestbookData, ensure_ascii=False).encode('utf8')
            return Response(jsonStr, content_type="application/json;charset=utf-8")
    
    def post(self):
        # json으로 받는다.
        args = parser.parse_args()
        sql = """
            insert into guestbook(title, contents, writer, wdate)
            values(%s, %s, %s, now())
        """
        # 튜플이라 괄호해야된다.
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
    
api.add_resource(Guestbook, '/rest_guestbook/list',
                            '/rest_guestbook/view/<int:id>',
                            # '/rest_guestbook',
                            '/rest_guestbook/save',
                            '/rest_guestbook/<int:id>')

if __name__ == '__main__':
    pass



# (myflask) C:\아나콘다\flask_workspace\myproject>set FLASK_APP=hello 
# (myflask) C:\아나콘다\flask_workspace\myproject>flask run
# http://localhost:5000/rest_guestbook/list
# http://localhost:5000/rest_guestbook/1, # http://localhost:5000/rest_guestbook/view/1
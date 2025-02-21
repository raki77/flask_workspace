from flask import (request, Blueprint, redirect, flash, render_template)
# from flask_restful import Resource, Api, reqparse
# import json
from . import DBModule


# __init__.py 안에 다 있어야 하는데, 그래서 연결작업 : BluePrint 모듈 담당한다.
# Blueprint 객체 생성
# /guestbook 으로 시작하는 url은 모두 이 모듈이 처리한다.
blueprint = Blueprint('guestbook', __name__, url_prefix="/guestbook")
@blueprint.route("/")
def guestbook():
    return "<H1>Guestbook</H1>"

@blueprint.route("/list")
def guestbook_list():
    sql = '''
        select A.id, A.title, A.writer, 
        date_format(A.wdate, '%%Y-%%m-%%d') wdate
        from guestbook A
    '''
    db = DBModule.Database()
    rows = db.executeAll(sql)
    db.close()
    return render_template("/guestbook/list.html", guestbookList=rows)


#http://127.0.0.1:5000/guestbook/view/1
@blueprint.route("/view/<int:id>")
def guestbook_view(id):
    sql = '''
        select A.id, A.title, A.writer, A.contents,
        date_format(A.wdate, '%%Y-%%m-%%d') wdate
        from guestbook A
        where id=%s
    '''
    db = DBModule.Database()
    row = db.executeOne(sql, (id,))
    db.close()
    return render_template("/guestbook/view.html", guest=row)

@blueprint.route("/write")
def guestboo_write():
    return render_template("/guestbook/write.html")

@blueprint.route("/save", methods=["POST"])
def guestbook_save():
    title = request.form["title"]
    writer = request.form["writer"]
    contents = request.form["contents"]
    
    # 서버에 남아있는 캐쉬를 삭제 시킴
    # 폼태그를 통해서 입력값들을 서버로 전송해서 받아오면
    # 값 전체를 삭제시킨다.
    sql = """
        insert into guestbook(title, writer, contents, wdate) values 
        (%s, %s, %s, NOW())
    """ 
    db = DBModule.Database()
    db.execute(sql, (title, writer, contents))
    db.close()
    return redirect("/guestbook/list")


# pip install flask_restful
#app = Blueprint('guestbook', __name__)
# restful api 객체를 생성한다. 매개변수로 Flask 객체를 전달해야 한다.
# api = Api(app)

# db = DBModule.Database()
# parser = reqparse.RequestParser()
# parser.add_argument('id')
# parser.add_argument('title')
# parser.add_argument('contents')
# parser.add_argument('writer')

# class Guestbook(Resource):
#     def get(self, id=None):
#         if id is None:
#             sql = """
#                 select id, title, contents, writer,
#                 date_format(wdate, '%%y-%%m-%%d') wdate
#                 from guestbook
#             """
#             guestbookData = db.executeAll(sql)
#             jsonStr = json.dumps(guestbookData, ensure_ascii=False).encode('utf8')
#             return Response(jsonStr, content_type="application/json;charset=utf-8")
#         else :
#             sql = """
#                 select id, title, contents, writer,
#                 date_format(wdate, '%%y-%%m-%%d') wdate
#                 from guestbook where id=%s
#             """
#             guestbookData = db.executeOne(sql, (id,))
#             jsonStr = json.dumps(guestbookData, ensure_ascii=False).encode('utf8')
#             return Response(jsonStr, content_type="application/json;charset=utf-8")
    
#     def post(self):
#         args = parser.parse_args()
#         sql = """
#             insert into guestbook(title, contents, writer, wdate)
#             values(%s, %s, %s, now())
#         """
#         db.execute(sql, (args['title'], 
#                          args['contents'], 
#                          args['writer']))
#         return {"result":"200ok"}
    
#     def put(self):
#         args = parser.parse_args()
#         sql = """
#             update guestbook set title=%s, contents=%s, writer=%s
#             where id=%s
#         """
#         db.execute(sql, (args['title'], args['contents'], args['writer'], args['id']))
#         return {"result" : "200ok"}
    
#     def delete(self, id=None):
#         args = parser.parse_args()
#         print("id=", id)
#         sql = """
#             delete from guestbook where id=%s
#         """
#         db.execute(sql, (id))
#         return {"result": "200ok"}
    
# api.add_resource(Guestbook, '/guestbook/list',
#                             '/guestbook/view/<int:id>',
#                             '/guestbook',
#                             '/guestbook/<int:id>')

# if __name__ == '__main__':
#     pass
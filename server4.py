
from flask import Flask
from flask import render_template, request
import pymongo
from pymongo import MongoClient 
from pymongo.collection import ReturnDocument


app = Flask(__name__)

# db 연동- 목록 가져오기 
from pymongo import MongoClient
conn = MongoClient("mongodb://user01:1234@127.0.0.1:27017/")
db = conn.mydb 

# collection 생성
guestbook = db.guestbook # 새로운 컬랙션 생성하기 
customSequences = db.customSequences  # 시퀀스 관리 컬렉션

# 시퀀스 컬렉션이 존재하지 않으면 생성
if customSequences.count_documents({"_id": "guestbook"}) == 0:
    customSequences.insert_one({"_id": "guestbook", "seq": 0})

def get_sequence(name):   
    document = db.customSequences.find_one_and_update(
        {"_id":"guestbook"}, 
        {"$inc": {"seq":1}}, 
        return_document=ReturnDocument.AFTER
    )
    return document['seq']
 
@app.route("/")
def hello():
    return "Hello, Python!!!"

# 게시판 title, contents, writer, wdate 하나 - dict
# 여러개일 경우 list( dict1, dict2, dict3,,,)
# boardData = [
#     {"id":1, "title":"제목1", "writer":"홍길동", "contents":"내용1"},
#     {"id":2, "title":"제목2", "writer":"임꺽정", "contents":"내용2"},
#     {"id":3, "title":"제목3", "writer":"장길산", "contents":"내용3"},
#     {"id":4, "title":"제목4", "writer":"홍경래", "contents":"내용4"},
#     {"id":5, "title":"제목5", "writer":"이장옥", "contents":"내용5"}
# ] 

id = get_sequence('guestbook')
guestbook.insert_one({
    "id": id,
    "title": f"제목{id}",
    "contents": f"내용{id}",
    "writer": f"홍길동{id}",
    "wdate": "2019-03-15",
    "age": 23
})

rows = db.guestbook.find()
print(type(rows))
for row in rows :
    print(row)

@app.route("/board/list")
def board_list():
    m_list = list(guestbook.find({}, {"_id": 0}))  
    return render_template("board_list.html", boardList=m_list)

if __name__ == "__main__":
    app.run()


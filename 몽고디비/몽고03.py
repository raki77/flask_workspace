import pymongo
from pymongo import MongoClient 
from pymongo.collection import ReturnDocument

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
    
'''
db.customSequences.insert({"_id": "guestbook",  seq:0})
db.customSequences.findAndModify({'query': { '_id':'guestbook'}, update: {'$inc':{seq:1}}, 'new': true	})
'''
def get_sequence(name):   
    document = db.customSequences.find_one_and_update(
        {"_id":"guestbook"}, 
        {"$inc": {"seq":1}}, 
        return_document=ReturnDocument.AFTER
    )
    #print(document.get('sec'))
    return document['seq']

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
for row in rows :
    print(row)

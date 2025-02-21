import pymongo
from pymongo import MongoClient 

# db 연동- 목록 가져오기 
from pymongo import MongoClient
client = MongoClient("mongodb://user01:1234@127.0.0.1:27017/")
db = client.mydb 
rows = db.person.find()
for row in rows :
    print(row)
    #print(row['_id'], row['name'], row['gender'])

    


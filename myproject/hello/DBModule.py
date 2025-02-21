import pymysql
import pymysql.cursors

# 디비 처리 전담 모듈
class Database:
    # 생성자
    # 파이썬은 오버로딩을 허용하지 않는다.
    # 동일한 이름의 함수를 못 만듬
    # 매개변수로 self를 데리고 다녀야 한다.
    # 객체자신의 기리키는게 self이다.
    # 대부분의 다른언어는 변수를 여기에 선언 (클래스변수로 알아서)
    # 맨처음에 클래스 정의시 딱 한번 만든다.
    def __init__(self):
        # 함수를 만들긴 만들건데 함수 몸통은 나중에 만들자.
        # pass
        self.db = pymysql.connect(host='localhost', user='user01', password='2718', db='mydb', port=3306)
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
        # 데이터 읽고 쓰기 담당 클래스 -> tuple 타입 -> dict 타입으로 전환
        # db라는 변수와 cursor 변수를 만드는데 self가 안붙으면 지역변수라 사라짐
        # self가 있어야 클래스 변수가 된다.
        
    # insert, delete, update
    def execute(self, query, args={}):        
        self.cursor.execute(query, args)
        # 파이선 mysql은 commit 안하면 디비 반영 안된다.
        self.db.commit()
    
    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row
    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        rows = self.cursor.fetchall()
        return rows
    def close(self):
        self.db.close()
        

if __name__ == "__main__":
    db = Database()
    db.execute("""
               insert into guestbook(title, writer, contents, wdate) values 
               (%s, %s, %s, NOW())
               """, ('테스트 제목', '테스트 작성자', '테스트 내용'))
    rows = db.executeAll("select * from guestbook")
    for row in rows:
        print(row)
    
    db.close()
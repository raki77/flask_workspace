from flask import Flask, redirect, url_for
from flask import render_template
from flask import request
from flask import session


app = Flask(__name__)

@app.route('/')
def index():
   return 'Welcome My Home'

@app.route('/admin')
def hello_admin():
    return 'Hello Admin'

@app.route('/guest/<guest>')
def hello_guest(guest):
   return f'Hello {guest} as Guest'
   #return 'Hello %s as Guest' % guest

@app.route('/user/<name>')
def hello_user(name):
   if name =='admin':
      return redirect(url_for('hello_admin'))
   else:
      return redirect(url_for('hello_guest', guest = name))


@app.route('/user/id/<int:userId>') 
def showUserProfileById(userId): 
   return 'USER ID : %d' % userId


@app.route("/write")
def write():
	return render_template("write.html")

#get방식 
@app.route("/save", methods=['GET', 'POST'])
def board1():           
   if request.method == "GET" :    
      username = request.values['username']
      age = request.values['age']      
   else: 
      username = request.form['username']
      age = request.form['age']
   # return f"<h1> {request.method}방식 username : {username}, age: {age}</h1>"
   return render_template("save.html", username=username, age=age)

# 덧셈 화면
@app.route("/add")
def add1():
	return render_template("add.html")

# 덧셈처리
@app.route("/addCalc", methods=['GET'])
def addCalc1():    
    try:
        val01 = int(request.values.get('val01', 0))  # 기본값을 0으로 설정
        val02 = int(request.values.get('val02', 0))
        result = val01 + val02
        return render_template("addResult.html", val01=val01, val02=val02, result=result)
    except ValueError:
        return "Invalid input. Please enter valid numbers.", 400

if __name__ == '__main__':
   app.run(debug = True) #서버 자동 재시작

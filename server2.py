from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, Python!!!"

@app.route("/hello")
def index():
    return "<h1>Welcome, Python!!!</h1>"

if __name__ == "__main__":
    app.run()


#실행 : python server1.py
#확인 : http://127.0.0.1:5000/

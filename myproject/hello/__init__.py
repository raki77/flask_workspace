import os
from flask import Flask
from . import guestbook
from . import rest_guestbook # 2025-02-24

def create_app(test_config=None):   
    app = Flask(__name__, instance_relative_config=True) # creates the flask instance
    app.config.from_mapping(SECRET_KEY='dev',)
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route('/')
    def index():
        return 'Hello, World!'
    
    # 파일결합 추가됨. 파일이 많아지면
    app.register_blueprint(guestbook.blueprint)
    app.register_blueprint(rest_guestbook.app)
    return app

""" 
myproject에서
set FLASK_APP=hello
flask run
"""
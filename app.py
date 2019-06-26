from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager, current_user
import models
import os

from resources.blogs import blogs_api
from resources.users import users_api
from resources.comments import comments_api

import config


login_manager = LoginManager()

app = Flask(__name__)

app.secret_key = config.SECRET_KEY
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id==userid)
    except models.DoesNotExist:
        return None
# CORS(blogs_api, origins=["http://localhost:3001", "http://mini-project4.herokuapp.com"], supports_credentials=True)
# CORS(users_api, origins=["http://localhost:3001", "http://mini-project4.herokuapp.com"], supports_credentials=True)
# CORS(comments_api, origins=["http://localhost:3001", "http://mini-project4.herokuapp.com"], supports_credentials=True)
CORS(blogs_api, origins=["http://localhost:3001"], supports_credentials=True)
CORS(users_api, origins=["http://localhost:3001"], supports_credentials=True)
CORS(comments_api, origins=["http://localhost:3001"], supports_credentials=True)

app.register_blueprint(blogs_api, url_prefix='/api/v1')
app.register_blueprint(users_api, url_prefix='/users')
app.register_blueprint(comments_api, url_prefix='/api/v1/blogs')

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    return 'hello david'

if 'ON_HEROKU' in os.environ:
    print('hitting ')
    models.initialize()
if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)
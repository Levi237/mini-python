from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager, current_user
import models

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

CORS(blogs_api, origins=["http://localhost:3000"], supports_credentials=True)
CORS(users_api, origins=["http://localhost:3000"], supports_credentials=True)
CORS(comments_api, origins=["http://localhost:3000"], supports_credentials=True)

app.register_blueprint(blogs_api, url_prefix='/api/v1')
app.register_blueprint(users_api, url_prefix='/users')
app.register_blueprint(comments_api, url_prefix='/api/v1')

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()
    ### most recent code added
    g.user = current_user
    #anywhere you can grab the full user object by running 
    g.user._get_current_object()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    return 'hello david'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)
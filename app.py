from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager
import models

from resources.blogs import blogs_api
from resources.users import users_api


DEBUG = True
PORT = 7000


app = Flask(__name__)

CORS(blogs_api, origins=["http://localhost:3000"], supports_credentials=True)
CORS(users_api, origins=["http://localhost:3000"], supports_credentials=True)

app.register_blueprint(blogs_api, url_prefix='/api/v1')
app.register_blueprint(users_api, url_prefix='/users')

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    return 'hello david'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
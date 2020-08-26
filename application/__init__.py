from flask import Flask 
from config import Config
from flask_mongoengine import MongoEngine
#Flask supports data persistency for Flask-SQLAlchemy, Flask-MongoEngine, flask-peewee and PonyORM
from flask_restplus import Api
from werkzeug.utils import cached_property
#With flask-restplus multiple endpoints are allowed in the route() decorator, also, decorate classes and methods

api = Api()

app = Flask(__name__)
app.config.from_object(Config)

#__name__ variable identifies the current application or module that is being rendered or passed to Flask

db = MongoEngine()
db.init_app(app)
api.init_app(app)

from application import routes
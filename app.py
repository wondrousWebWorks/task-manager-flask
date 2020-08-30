import os
from flask import Flask
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists('env.py'):
    import env

APP = Flask(__name__)

APP.config['MONGO_DBNAME'] = os.environ.get("MONGO_DBNAME")
APP.config['MONGO_URI'] = os.environ.get("MONGO_URI")
APP.secret_key = os.environ.get("SECRET_KEY")


@APP.route('/')
def index():
    return "Hello, world"

if __name__ == '__main__':
    APP.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=os.environ.get('DEBUG'),
            )
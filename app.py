import os
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists('env.py'):
    import env

APP = Flask(__name__)

APP.config['MONGO_DBNAME'] = os.environ.get("MONGO_DBNAME")
APP.config['MONGO_URI'] = os.environ.get("MONGO_URI")
APP.secret_key = os.environ.get("SECRET_KEY")

MONGO = PyMongo(APP)


@APP.route('/')
@APP.route('/get_tasks')
def get_tasks():
    """Display the Task Manager page"""

    tasks = MONGO.db.tasks.find()

    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    APP.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=os.environ.get('DEBUG'),
            )
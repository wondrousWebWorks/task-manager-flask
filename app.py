import os
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

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


@APP.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = MONGO.db.users.find_one(
            {'username': request.form.get('username').lower()})

        if existing_user:
            flash('Username already exists')
            return redirect(url_for('register'))

        register = {
            'username': request.form.get('username').lower(),
            'password': generate_password_hash(request.form.get('password'))
        }
        MONGO.db.users.insert_one(register)

        # put the new user into 'session cookie'
        session['user'] = request.form.get('username').lower()
        flash('Registration successfull')
    return render_template('register.html')


@APP.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # check if userna,e exists in db
        existing_user = MONGO.db.users.find_one(
            {"username": request.form.get('username').lower()})

        if existing_user:
            #ensure hashed password matches user input
            if check_password_hash(
                existing_user['password'], request.form.get('password')):
                    session['user'] = request.form.get('username').lower()
                    flash('Welcome, {}'.format(request.form.get('username')))
            else:
                flash('Incorrect Username and/or Password')
                return redirect(url_for('login'))

        else:
            #username doesn't exist
                flash('Incorrect Username and/or Password')
                return redirect(url_for('login'))

    return render_template('login.html')


if __name__ == '__main__':
    APP.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=os.environ.get('DEBUG'),
            )
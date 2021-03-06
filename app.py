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
    tasks = list(MONGO.db.tasks.find())
    return render_template('tasks.html', tasks=tasks)


@APP.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query')
    tasks = list(MONGO.db.tasks.find({'$text': {'$search': query}}))
    return render_template('tasks.html', tasks=tasks)


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
        return redirect(url_for('profile', username=session['user']))

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
                    flash('Welcome, {}'.format(
                        request.form.get('username')))
                    return redirect(url_for(
                        'profile', username=session['user']))
            else:
                flash('Incorrect Username and/or Password')
                return redirect(url_for('login'))

        else:
            #username doesn't exist
                flash('Incorrect Username and/or Password')
                return redirect(url_for('login'))

    return render_template('login.html')


@APP.route('/profile<username>', methods=['GET', 'POST'])
def profile(username):
    #grab the session user's name from the db'
    username = MONGO.db.users.find_one(
        {'username': session['user']})['username']

    if session['user']:
        return render_template('profile.html', username=username)

    return redirect(url_for('login'))


@APP.route('/logout')
def logout():
    # remove user from session cookies
    flash('You have been logged out')
    session.pop('user')
    return redirect(url_for('login'))


@APP.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        is_urgent = 'on' if request.form.get('is_urgent') else 'off'
        task = {
            'category_name': request.form.get('category_name'),
            'task_name': request.form.get('task_name'),
            'task_description': request.form.get('task_description'),
            'is_urgent': is_urgent,
            'due_date': request.form.get('due_date'),
            'created_by': session['user'],
        }
        MONGO.db.tasks.insert_one(task)
        flash('Task Successfully Added')
        return redirect(url_for('get_tasks'))

    categories = MONGO.db.categories.find().sort('category_name', 1)
    return render_template('add_task.html', categories=categories)


@APP.route("/edit_task/<task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    if request.method == 'POST':
        is_urgent = 'on' if request.form.get('is_urgent') else 'off'
        submit = {
            'category_name': request.form.get('category_name'),
            'task_name': request.form.get('task_name'),
            'task_description': request.form.get('task_description'),
            'is_urgent': is_urgent,
            'due_date': request.form.get('due_date'),
            'created_by': session['user'],
        }
        MONGO.db.tasks.update({'_id': ObjectId(task_id)}, submit)
        flash('Task Successfully Updated')

    task = MONGO.db.tasks.find_one({"_id": ObjectId(task_id)})
    categories = MONGO.db.categories.find().sort("category_name", 1)
    return render_template("edit_task.html", task=task, categories=categories)


@APP.route('/delete_task/<task_id>')
def delete_task(task_id):
    MONGO.db.tasks.remove({'_id': ObjectId(task_id)})
    flash('Task Successfully Deleted')
    return redirect(url_for('get_tasks'))


@APP.route('/get_categories')
def get_categories():
    categories = list(MONGO.db.categories.find().sort('category_name', 1))
    return render_template('categories.html', categories=categories)


@APP.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        category = {
            'category_name': request.form.get('category_name')
        }
        MONGO.db.categories.insert_one(category)
        flash('New Category Added')
        return redirect(url_for('get_categories'))

    return render_template('add_category.html')


@APP.route('/edit_category/<category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    if request.method == 'POST':
        submit = {
            'category_name': request.form.get('category_name')
        }
        MONGO.db.categories.update({'_id': ObjectId(category_id)}, submit)
        flash('Category Successfully Updated')
        return redirect(url_for('get_categories'))

    category = MONGO.db.categories.find_one({'_id': ObjectId(category_id)})
    return render_template('edit_category.html', category=category)


@APP.route('/delete_category/<category_id>')
def delete_category(category_id):
    MONGO.db.categories.remove({'_id': ObjectId(category_id)})
    flash('Category Successfully Deleted')
    return redirect(url_for('get_categories'))



if __name__ == '__main__':
    APP.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=os.environ.get('DEBUG'),
            )
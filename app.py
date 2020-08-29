import os
from flask import Flask

if os.path.exists('env.py'):
    import env

APP = Flask(__name__)

@APP.route('/')
def index():
    return "Hello, world"

if __name__ == '__main__':
    APP.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=os.environ.get('DEBUG'),
            )
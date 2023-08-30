from flask import Blueprint

debug = Blueprint('debug', __name__)

@debug.route('/home')
def home():
        return "Hello world!"

    

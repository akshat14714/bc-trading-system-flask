from flask import render_template, Blueprint
from flask_login import current_user

home = Blueprint('home', __name__)


@home.route('/')
def homepage():
    return render_template('home/index.html', title="Welcome")


# @home.route()

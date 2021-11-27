from flask import *

from app import db
from ..user.model import User

home = Blueprint('home', __name__)


@home.route('/')
def homepage():
    # if 'username' in session:
    #     user = User.query.filter(User.username == session['username']).first()
    #     return render_template('client/profile.html', user=user)
    return render_template('home/index.html', title="Welcome")


# @home.route()

from flask import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from app import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
import re

from flask_cors import CORS

mod_user = Blueprint('user', __name__)
CORS(mod_user)

global a
a = ''


# @mod_user.route('/', methods=['GET'])
# def func():
#     if 'username' not in session and 'email' not in session:
#         return redirect('/login')
#     return render_template('index.html')

@mod_user.route('/')
@mod_user.route('/login', methods=['GET', 'POST'])
def login():
    display_message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        # print(request.form['password'])
        # print(generate_password_hash('password'))
        password = request.form['password']
        # cursor = mysql.get_db().cursor()
        # cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        # account = cursor.fetchone()
        user = User.query.filter(User.username == username).first()
        # print(user.password)
        # print(password)
        print(user.check_password(password))
        if user is None or not user.check_password(password):
            return make_response('Invalid Username or Password', 400, None)
        print(user)
        # if user:
        session['loggedin'] = True
        session['id'] = user.id
        session['username'] = user.username
        msg = 'Logged in successfully !'
        return render_template('index.html')
        # else:
        #     msg = 'Incorrect username / password !'
    return render_template('login.html')


@mod_user.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        print(request.form['password'])
        password = generate_password_hash(request.form['password'])
        email = request.form['email']
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        mobile_phone = request.form['mobilephone']
        user = User.query.filter(User.username == username).first()
        if user:
            msg = 'User already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not re.match(r'[0-9]{10}', mobile_phone):
            msg = 'Phone number must be of only 10 digits !'
        elif not username or not password or not email or not first_name or not last_name or not mobile_phone:
            msg = 'Please fill out the form !'
        else:
            user = User(username, email, first_name, last_name, password, mobile_phone)
            print(password)
            db.session.add(user)
            db.session.commit()
            msg = 'You have successfully registered !'
            return redirect('/')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@mod_user.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
        session.pop('id')
        session.pop('loggedin')
    return redirect('/login')

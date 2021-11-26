import datetime
import os

from flask import Flask, session, render_template, request, redirect, url_for
# from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy
import re

from app import app

from flask_cors import CORS

# config_name = os.getenv('FLASK_CONFIG')
# print(config_name)
# app = create_app()

CORS(app)

# app = Flask(__name__)

# app_config = {
#     "DEBUG": True
# }
# app.config.from_mapping(app_config)

# db = SQLAlchemy(app=app)

# initialize all the key value pairs required for the mysql connection
# app.secret_key = 'password123'
# app.config['MYSQL_DATABASE_USER'] = 'sql_admin'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'progamut'
# app.config['MYSQL_DATABASE_DB'] = 'btctradingflask'

# mysql = MySQL(app)


# make session time 5 min
@app.before_request
def make_session_permanent():
    app.permanent_session_lifetime = datetime.timedelta(minutes=15)


# @app.route("/")
# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     display_message = ''
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
#         username = request.form['username']
#         password = request.form['password']
#         cursor = mysql.get_db().cursor()
#         cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
#         account = cursor.fetchone()
#         print(account)
#         if account:
#             session['loggedin'] = True
#             session['id'] = account[0]
#             session['username'] = account[1]
#             msg = 'Logged in successfully !'
#             return render_template('index.html', msg=display_message)
#         else:
#             msg = 'Incorrect username / password !'
#     return render_template('login.html', msg=display_message)
#
#
# @app.route('/logout')
# def logout():
#     session.pop('loggedin', None)
#     session.pop('id', None)
#     session.pop('username', None)
#     return redirect(url_for('login'))
#
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     msg = ''
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form['email']
#         firstName = request.form['firstname']
#         lastName = request.form['lastname']
#         mobilePhone = request.form['mobilephone']
#         # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor = mysql.get_db().cursor()
#         cursor.execute('SELECT * FROM accounts WHERE username = %s OR email = %s', (username, email))
#         account = cursor.fetchone()
#         if account:
#             msg = 'Account already exists !'
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             msg = 'Invalid email address !'
#         elif not re.match(r'[A-Za-z0-9]+', username):
#             msg = 'Username must contain only characters and numbers !'
#         elif not re.match(r'[0-9]{10}', mobilePhone):
#             msg = 'Phone number must be of only 10 digits !'
#         elif not username or not password or not email or not firstName or not lastName or not mobilePhone:
#             msg = 'Please fill out the form !'
#         else:
#             cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email,))
#             mysql.connection.commit()
#             msg = 'You have successfully registered !'
#     elif request.method == 'POST':
#         msg = 'Please fill out the form !'
#     return render_template('register.html', msg=msg)


# @app.route('/')
# def index():
#     return 'Hello, Flask!'


if __name__ == '__main__':
    app.run(debug=True)

# from flask_login import UserMixin
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    mobile_phone = db.Column(db.String(10), nullable=False, unique=True)
    type = db.Column(db.Integer, nullable=False, default=1)
    level = db.Column(db.Integer, nullable=True)

    def __init__(self, username, email, first_name, last_name, password, mobile_phone):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.mobile_phone = mobile_phone

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def serialize(self):
        return {'username': self.username,
                'email': self.email,
                'First Name': self.first_name,
                'Last Name': self.last_name,
                'password': self.password,
                'Mobile Phone': self.mobile_phone}

    def __repr__(self):
        return "User<%d> %s" % (self.id, self.username)

    # @property
    # def password(self):
    #     raise AttributeError('password is not readable')
    #
    # @password.setter
    # def password(self, password):
    #     self.password = generate_password_hash(password)
    #
    # def verify_password(self, password):
    #     return check_password_hash(self.password, password)
    #
    # def __repr__(self):
    #     return 'User: <>'.format(self.username)

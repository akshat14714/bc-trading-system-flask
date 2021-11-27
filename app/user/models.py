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
    type = db.Column(db.Integer, nullable=False, default=3)
    level = db.Column(db.Integer, nullable=True)
    street = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zipcode = db.Column(db.String(10))
    bitcoin_balance = db.Column(db.Float, default=0.0)
    fiat_balance = db.Column(db.Float, default=0.0)
    total_transaction = db.Column(db.Float, default=0.0)

    MANAGER = 1
    TRADER = 2
    CLIENT = 3

    def __init__(self, username, email, first_name, last_name, password, mobile_phone, street, city, state, zipcode,
                 bitcoin_balance=0, fiat_balance=0, total_transaction=0):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.mobile_phone = mobile_phone
        if self.type == self.CLIENT:
            self.level = 1
        self.street = street
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.bitcoin_balance = bitcoin_balance
        self.fiat_balance = fiat_balance
        self.total_transaction = total_transaction

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def serialize(self):
        return {'username': self.username,
                'email': self.email,
                'First Name': self.first_name,
                'Last Name': self.last_name,
                'password': self.password,
                'Mobile Phone': self.mobile_phone,
                'Type': self.type,
                'Street': self.street,
                'City': self.city,
                'ZipCode': self.zipcode}

    def __repr__(self):
        return "User<%d> %s" % (self.id, self.username)

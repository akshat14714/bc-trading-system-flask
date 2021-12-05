from flask import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from datetime import datetime

import config
from app import db, utils
from .model import User
from ..changelog.model import ChangeLog
from ..transaction.model import Transaction
from ..trade.model import Trade
from werkzeug.security import generate_password_hash, check_password_hash
import re

from flask_cors import CORS

mod_user = Blueprint('user', __name__)
CORS(mod_user)


@mod_user.route('/login', methods=['GET', 'POST'])
def login():
    display_message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter(User.username == username).first()
        if user is None or not user.check_password(password):
            return make_response('Invalid Username or Password', 400, None)
        # if user:
        session['loggedin'] = True
        session['user_id'] = user.id
        session['username'] = user.username
        session['usertype'] = user.user_type
        # msg = 'Logged in successfully !'
        if user.user_type == User.CLIENT:
            return redirect('/client/profile')
        elif user.user_type == User.TRADER:
            return redirect('/trader/profile')
    return render_template('login.html')


@mod_user.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        print(request.form['password'])
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        mobile_phone = request.form['mobilephone']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
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
            user = User(username, email, first_name, last_name, password, mobile_phone, User.CLIENT, street, city,
                        state, zipcode)
            db.session.add(user)
            db.session.commit()
            msg = 'You have successfully registered !'
            return redirect('/login')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@mod_user.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
        session.pop('user_id')
        session.pop('usertype')
        session.pop('loggedin')
    return redirect('/')


@mod_user.route('/profile')
def get_user_profile():
    if 'username' in session:
        if session['usertype'] == User.CLIENT:
            return  redirect('/client/profile')
        elif session['usertype'] == User.TRADER:
            return redirect('/trader/profile')

    return redirect('/login')


@mod_user.route('/client/profile', methods=['GET'])
def client_profile():
    if 'username' not in session or session['usertype'] != User.CLIENT:
        abort(403)

    user_ = User.query.filter(User.username == session['username']).first()
    deposits_ = Transaction.query.filter_by(client_id=user_.id, xid_type='add_fund')
    trades_ = Trade.query.filter_by(client_id=user_.id)
    return render_template('client/profile.html', user=user_, deposits=deposits_, trades=trades_)


@mod_user.route('/client/deposit_fiat', methods=['GET', 'POST'])
def deposit_fiat():
    if 'username' not in session or session['usertype'] != User.CLIENT:
        abort(403)

    if request.method == 'POST':
        client_id = session['user_id']
        amount = float(request.form['fiat_deposit_amount'])

        user = User.query.filter(User.id == client_id).first()
        # user.fiat_balance += amount

        transaction = Transaction(xid_type='add_fund',
                                  status='pending',
                                  client_id=user.id,
                                  timestamp=datetime.now(),
                                  fiat_amount=amount)
        db.session.add(transaction)
        db.session.flush()

        changelog = ChangeLog(timestamp=datetime.now(),
                              xid=transaction.id,
                              status='pending',
                              xid_type='add_fund',
                              client_id=user.id)
        db.session.add(changelog)

        db.session.commit()

        return redirect('/client/profile')

    return render_template('client/deposit_fiat.html')


@mod_user.route('/client/trade', methods=['GET', 'POST'])
def trade():
    if 'username' not in session or session['usertype'] != User.CLIENT:
        abort(403)

    exchange_rate = utils.get_current_rate()

    user = User.query.filter(User.id == session['user_id']).first()
    account_ = {
        'bitcoin_balance': user.bitcoin_balance,
        'fiat_balance': user.fiat_balance,
        'level': user.level,
        'commission': config.commission_rates[user.level],
        'exchange_rate': exchange_rate
    }

    if request.method == 'POST':
        password = request.form['password']
        if not user.check_password(password):
            abort(403)

        valid = True
        btc_amount = float(request.form['bitcoin_amount'])
        type_of_trade = request.form['buysell']
        commission_type = request.form['commissiontype']

        btc_total = 0.0
        usd_total = 0.0

        total_usd_amount = btc_amount * exchange_rate
        commission = config.commission_rates[user.level] * total_usd_amount / 100

        if type_of_trade == 'buy':
            usd_total = total_usd_amount
        else:
            btc_total = btc_amount

        if commission_type == 'usd':
            usd_total += commission
        else:
            btc_total += commission / exchange_rate

        if usd_total > user.fiat_balance:
            valid = False

        if btc_total > user.bitcoin_balance:
            valid = False

        # print(valid, usd_total, btc_total)

        if not valid:
            # flash("You don't have enough funds in your account!")
            return render_template('client/trade.html', title='Client Trading', account=account_)

        # user.total_transaction += total_usd_amount

        # if user.level == 1 and user.total_transaction >= config.TRANSACTION_AMOUNT_FOR_LEVEL_CHANGE:
        #     user.level = 2

        trade_ = Trade(xid_type=type_of_trade,
                       status='pending',
                       client_id=user.id,
                       timestamp=datetime.now(),
                       fiat_amount=total_usd_amount,
                       bitcoin_amount=btc_amount,
                       exchange_rate=exchange_rate,
                       commission=commission,
                       commission_type=commission_type)

        db.session.add(trade_)
        db.session.flush()

        changelog = ChangeLog(timestamp=datetime.now(),
                              xid=trade_.id,
                              status='pending',
                              xid_type=type_of_trade,
                              client_id=user.id)
        db.session.add(changelog)

        db.session.commit()

        # flash("You have successfully completed the transaction!")
        return redirect('/client/profile')

    return render_template('client/trade.html', title='Client Trading', account=account_)

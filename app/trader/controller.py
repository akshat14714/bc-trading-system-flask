from flask import *
from datetime import datetime
from sqlalchemy.sql.expression import and_
from sqlalchemy import func, desc
import sqlalchemy as sa

import config
from app import db, utils
from ..user.model import User
from ..trade.model import Trade
from ..transaction.model import Transaction
from ..changelog.model import ChangeLog

from flask_cors import CORS

trader = Blueprint('trader', __name__)
CORS(trader)


@trader.route('/trader/profile')
def get_trader_profile():
    if 'username' not in session or session['usertype'] != User.TRADER:
        abort(403)

    trades = Trade.query.filter_by(trader_id=session['user_id']).order_by(Trade.timestamp.desc())

    transactions = Transaction.query.filter_by(trader_id=session['user_id']).order_by(Transaction.timestamp.desc())

    return render_template('trader/profile.html', trades=trades, transactions=transactions)


@trader.route('/trader/pending_deposits')
def list_pending_deposits():
    if 'username' not in session or session['usertype'] != User.TRADER:
        abort(403)

    pending_deposits = Transaction.query.filter_by(xid_type='add_fund', status='pending').order_by(
        Transaction.timestamp)
    if pending_deposits.count() == 0:
        pending_deposits = None

    return render_template('trader/pending_deposits.html', pending_deposits=pending_deposits)


@trader.route('/trader/update_deposit/<string:action>/<int:xid>', methods=['GET', 'POST'])
def update_pending_deposit(action, xid):
    if 'username' not in session or session['usertype'] != User.TRADER:
        abort(403)

    deposit = Transaction.query.get_or_404(xid)

    if deposit.status == 'pending':
        msg = ''
        deposit.trader_id = session['user_id']
        client = User.query.get_or_404(deposit.client_id)
        if action == 'approve':
            deposit.status = 'approved'
            client.fiat_balance += deposit.fiat_amount
            msg = 'You have approved the deposit ID:' + str(id)
        elif action == 'cancel':
            deposit.status = 'cancelled'
            msg = 'You have cancelled the deposit ID:' + str(id)

        changelog = ChangeLog(timestamp=datetime.now(),
                              xid=xid,
                              status=deposit.status,
                              xid_type='add_fund',
                              client_id=client.id,
                              trader_id=session['user_id'])
        db.session.add(changelog)

        db.session.commit()

        # if msg != '':
        #     flash(msg)
    # else:
        # flash("The selected deposit is not in pending status!")
    return redirect(url_for('trader.list_pending_deposits'))


@trader.route('/trader/pending_trades')
def list_pending_trades():
    if 'username' not in session or session['usertype'] != User.TRADER:
        abort(403)

    pending_trades = Trade.query.filter_by(status='pending').order_by(Trade.timestamp)
    if pending_trades.count() == 0:
        pending_trades = None

    return render_template('trader/pending_trades.html', pending_trades=pending_trades)


@trader.route('/trader/update_trade/<string:action>/<int:xid>', methods=['GET', 'POST'])
def update_trade(action, xid):
    trade = Trade.query.get_or_404(xid)
    client = User.query.get_or_404(trade.client_id)
    if trade.status == 'pending':
        msg = ''
        bitcoin_price = trade.bitcoin_amount * trade.exchange_rate
        trade.trader_id = session['user_id']
        bitcoin_amount = trade.bitcoin_amount

        if action == 'approve':
            if trade.xid_type == 'buy':
                if trade.commission_type == 'usd':
                    bitcoin_price += trade.commission
                else:
                    bitcoin_amount -= trade.commission
                client.bitcoin_balance += bitcoin_amount
                client.fiat_balance -= bitcoin_price
            else:
                if trade.commission_type == 'usd':
                    bitcoin_price -= trade.commission
                else:
                    bitcoin_amount += trade.commission
                client.bitcoin_balance -= bitcoin_amount
                client.fiat_balance += bitcoin_price

            client.total_transaction += trade.fiat_amount

            if client.level == 1 and client.total_transaction >= config.TRANSACTION_AMOUNT_FOR_LEVEL_CHANGE:
                client.level = 2

            trade.status = 'approved'
            msg = 'You have approved the order:' + str(xid)
        elif action == 'cancel':
            trade.status = 'cancelled'
            msg = 'You have canceled the order:' + str(xid)

        changelog = ChangeLog(timestamp=datetime.now(),
                              xid=trade.id,
                              status=trade.status,
                              xid_type=trade.xid_type,
                              client_id=client.id,
                              trader_id=session['user_id'])
        db.session.add(changelog)

        db.session.commit()

        # if msg != '':
        #     flash(msg)
    # else:
        # flash("The selected order is not in pending status!")
    return redirect(url_for('trader.list_pending_trades'))


@trader.route('/trader/client_search/<int:is_search>', methods=['POST', 'GET'])
def get_client_data(is_search=0):
    if is_search:
        form_data = request.args
        if form_data['Condition']:
            clients = User.query.filter(
                and_(getattr(User, form_data['Field']).like('%' + form_data['Condition'] + '%'), User.user_type == 3))
            # print(clients)
            # for client in clients:
            #     print(client)
        else:
            # flash("Enter some value in search key!")
            return render_template('trader/client_search.html', title='Find clients', is_search=0)

        return render_template('trader/client_search.html', title='Find clients', clients=clients, is_search=1)
    else:
        return render_template('trader/client_search.html', title='Find clients', is_search=0)


@trader.route('/trader/client_info/<int:id>', methods=['GET', 'POST'])
def get_client_info(id):
    client = User.query.filter_by(id=id)
    trades = Trade.query.filter_by(client_id=id).order_by(desc(Trade.timestamp))
    deposits = Transaction.query.filter_by(client_id=id).order_by(desc(Transaction.timestamp))
    return render_template('trader/client_info.html', title='Client information', client=client, deposits=deposits,
                           trades=trades)


@trader.route('/trader/trade_client/<int:id>', methods=['POST', 'GET'])
def trade_for_client(id):
    if 'username' not in session or session['usertype'] != User.TRADER:
        abort(403)

    exchange_rate = utils.get_current_rate()

    user = User.query.filter(User.id == session['user_id']).first()

    client = User.query.filter(User.id == id).first()
    account_ = {
        'client_id': client.id,
        'bitcoin_balance': client.bitcoin_balance,
        'fiat_balance': client.fiat_balance,
        'level': client.level,
        'commission': config.commission_rates[client.level],
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
        commission = config.commission_rates[client.level] * total_usd_amount / 100

        if type_of_trade == 'buy':
            usd_total = total_usd_amount
        else:
            btc_total = btc_amount

        if commission_type == 'usd':
            usd_total += commission
        else:
            btc_total += commission / exchange_rate

        if usd_total > client.fiat_balance:
            valid = False

        if btc_total > client.bitcoin_balance:
            valid = False

        # print(valid, usd_total, btc_total)

        if not valid:
            # flash("You don't have enough funds in your account!")
            return render_template('trader/client_trade.html', title='Trade for Client', account=account_)

        trade_ = Trade(xid_type=type_of_trade,
                       status='pending',
                       client_id=client.id,
                       trader_id=session['user_id'],
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
                              client_id=client.id,
                              trader_id=session['user_id'])
        db.session.add(changelog)

        db.session.commit()

        # flash("You have successfully completed the transaction!")
        return redirect('/trader/client_search/0')

    return render_template('trader/client_trade.html', title='Trade for Client', account=account_)


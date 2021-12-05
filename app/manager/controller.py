from flask.globals import session
from app.user.model import User
from app.trade.model import Trade
from app.transaction.model import Transaction
from flask import *
from flask_cors import CORS

mod_manager = Blueprint('manager', __name__)
CORS(mod_manager)


def check_manager():
    if 'username' not in session or session['usertype'] != User.MANAGER:
        abort(403)


@mod_manager.route('/manager/profile')
def get_manager_profile():
    check_manager()

    user = User.query.filter_by(id=session['user_id'])

    trades = Trade.query.all()
    transactions = Transaction.query.all()

    for trade in trades:
        print(trade)

    return render_template('manager/manager_home.html', user=user, trades=trades, transactions=transactions)


@mod_manager.route('/manager/clients', methods=['GET', 'POST'])
def list_clients():
    check_manager()
    clients = User.query.filter_by(user_type=User.CLIENT)
    return render_template('manager/clients/clients.html', clients=clients, title="Clients")


@mod_manager.route('/manager/traders', methods=['GET', 'POST'])
def list_traders():
    check_manager()
    traders = User.query.filter_by(user_type=User.TRADER)
    return render_template('manager/traders/traders.html', traders=traders, title='Traders')


@mod_manager.route('/manager/add_client', methods=['GET', 'POST'])
def add_client():
    check_manager()
    return render_template('manager/trader_client.html')


@mod_manager.route('/manager/add_trader', methods=['GET', 'POST'])
def add_trader():
    check_manager()
    if request.method == 'POST':
        if User.query.filter_by(username=request.form["username"]).first():
            return render_template('manager/traders/trader.html')
        return redirect("/manager/traders")
    return render_template('manager/trader_client.html')

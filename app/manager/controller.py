from flask.globals import session
from app.user.model import User
from flask import *
from flask_cors import CORS

mod_manager = Blueprint('manager', __name__)
CORS(mod_manager)


def check_manager():
    if 'username' not in session or session['usertype'] != User.MANAGER:
        abort(403)


@mod_manager.route('/clients', methods=['GET', 'POST'])
def list_clients():
    check_manager()
    clients = User.query.filter_by(type=User.CLIENT)
    return render_template('manager/clients/clients.html', clients=clients, title="Clients")


@mod_manager.route('/traders', methods=['GET', 'POST'])
def list_traders():
    check_manager()
    traders = User.query.filter_by(type=User.TRADER)
    return render_template('manager/traders/traders.html', traders=traders, title='Traders')


@mod_manager.route('/add_client', methods=['GET', 'POST'])
def add_client():
    check_manager()
    return render_template('manager/trader_client.html')


@mod_manager.route('/add_trader', methods=['GET', 'POST'])
def add_trader():
    check_manager()
    if request.method == 'POST':
        if User.query.filter_by(username=request.form["username"]).first():
            return render_template('manager/traders/trader.html')
        return redirect("/traders")
    return render_template('manager/trader_client.html')

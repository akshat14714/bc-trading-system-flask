from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from dateutil.relativedelta import *

app = Flask(__name__)

app.config.from_object('config')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app.home.controller import home
from app.user.controller import mod_user
from app.trader.controller import trader
from app.manager.controller import mod_manager

app.register_blueprint(home)
app.register_blueprint(mod_user)
app.register_blueprint(trader)
app.register_blueprint(mod_manager)

db.create_all()


def update_client_status():
    import logging

    log = logging.getLogger('apscheduler.executors.default')
    log.setLevel(logging.INFO)  # DEBUG

    fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    h = logging.StreamHandler()
    h.setFormatter(fmt)
    log.addHandler(h)

    from user.model import User
    with db.app.app_context():
        clients = User.query.filter_by(user_type=User.CLIENT)

        for client in clients:
            if client.transactions > 100000:
                client.level = 1
            else:
                client.level = 0

        db.session.commit()


scheduler = BackgroundScheduler()
scheduler.add_job(func=update_client_status, trigger='cron', month='1-12', day='last', hour='23', minute='55')
scheduler.start()


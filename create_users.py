from app import db
from app.user.model import User


def create_trader():
    trader = User(username='bot_trader1',
                  email='bot_trader1@example.com',
                  first_name='Bot',
                  last_name='Trader1',
                  password='trader_hacker',
                  mobile_phone='1209348756')
    db.session.add(trader)
    db.session.commit()

from app import db
from app.user.model import User


def create_trader():
    trader = User(username='bot_trader1',
                  email='bot_trader1@example.com',
                  first_name='Bot',
                  last_name='Trader1',
                  password='trader_hacker',
                  mobile_phone='1209348756',
                  user_type=2)
    db.session.add(trader)
    db.session.commit()


def create_manager():
    trader = User(username='admin',
                  email='admin@example.com',
                  first_name='Admin',
                  last_name='Manager',
                  password='admin123',
                  mobile_phone='1234567890',
                  user_type=2)
    db.session.add(trader)
    db.session.commit()

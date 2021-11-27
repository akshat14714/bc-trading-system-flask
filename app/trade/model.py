from sqlalchemy import ForeignKey
from datetime import datetime

from app import db


class Trade(db.Model):
    __tablename__ = 'trades'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    xid_type = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    client_id = db.Column(db.Integer, ForeignKey('users.id'))
    trader_id = db.Column(db.Integer, ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, nullable=False)
    fiat_amount = db.Column(db.Float, default=0)
    bitcoin_amount = db.Column(db.Float)
    exchange_rate = db.Column(db.Float)
    commission = db.Column(db.Float, default=0)
    commission_type = db.Column(db.String(10))

    def __init__(self, xid_type, status, client_id, trader_id=6, timestamp=datetime.now(), fiat_amount=0.0,
                 bitcoin_amount=0.0, exchange_rate=0.0, commission=0.0, commission_type='usd'):
        self.xid_type = xid_type
        self.status = status
        self.client_id = client_id
        self.trader_id = trader_id
        self.timestamp = timestamp
        self.fiat_amount = fiat_amount
        self.bitcoin_amount = bitcoin_amount
        self.exchange_rate = exchange_rate
        self.commission = commission
        self.commission_type = commission_type

    def serialize(self):
        return {'status': self.status,
                'client_id': self.client_id,
                'trader_id': self.trader_id,
                'timestamp': self.timestamp,
                'Fiat Amount': self.fiat_amount,
                'Bitcoins Amount': self.bitcoin_amount,
                'Exchange Rate': self.exchange_rate}

    def __repr__(self):
        return "Transaction<%d> %s, %s, %f" % (self.id, self.client_id, self.trader_id, self.fiat_amount)

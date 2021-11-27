from sqlalchemy import ForeignKey

from app import db


class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(30), nullable=False)
    client_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    trader_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    fiat_amount = db.Column(db.Float, default=0)

    def __init__(self, status, client_id, trader_id, timestamp, fiat_amount=0.0):
        self.status = status
        self.client_id = client_id
        self.trader_id = trader_id
        self.timestamp = timestamp
        self.fiat_amount = fiat_amount

    def serialize(self):
        return {'status': self.status,
                'client_id': self.client_id,
                'trader_id': self.trader_id,
                'timestamp': self.timestamp,
                'Fiat Amount': self.fiat_amount}

    def __repr__(self):
        return "Payment<%d> %s, %s, %f" % (self.id, self.client_id, self.trader_id, self.fiat_amount)

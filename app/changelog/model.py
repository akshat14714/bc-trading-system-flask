from sqlalchemy import ForeignKey

from app import db


class ChangeLog(db.Model):
    __tablename__ = 'changelogs'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    xid = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    xid_type = db.Column(db.String(20), nullable=False)
    client_id = db.Column(db.Integer, ForeignKey('users.id'))
    trader_id = db.Column(db.Integer, ForeignKey('users.id'))

    def __init__(self, timestamp, xid, status, xid_type, client_id, trader_id=2):
        self.timestamp = timestamp
        self.xid = xid
        self.status = status
        self.xid_type = xid_type
        self.client_id = client_id
        self.trader_id = trader_id

    def serialize(self):
        return {'timestamp': self.timestamp,
                'xid': self.xid,
                'status': self.status,
                'xid_type': self.xid_type,
                'client_id': self.client_id,
                'trader_id': self.trader_id}

    def __repr__(self):
        return "ChangeLog<%d> %d, %s, %d, %d" % (self.id, self.xid, self.status, self.xid_type, self.client_id)

from app import db


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.String)
    sender = db.Column(db.String)
    target = db.Column(db.String)
    message = db.Column(db.String)
    client_order_id = db.Column(db.String)
    details = db.Column(db.String)
    msgcat = db.Column(db.String)
    raw = db.Column(db.String(512))
    fields = db.Column(db.String(5120))

    def __init__(self, time, sender, target, message, client_order_id, details, msgcat, raw, fields):
        self.time = time
        self.sender = sender
        self.target = target
        self.message = message
        self.client_order_id = client_order_id
        self.details = details
        self.msgcat = msgcat
        self.raw = raw
        self.fields = fields

    def __repr__(self):
        return '<{},{},{},{},{},{},{},{},{},{}>'.format(self.id, self.time, self.sender, self.target, self.message,
                                                        self.client_order_id, self.details, self.msgcat, self.raw,
                                                        self.fields)

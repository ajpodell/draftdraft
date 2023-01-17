from models.base import db

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    username_first = db.Column(db.String())
    username_last = db.Column(db.String())

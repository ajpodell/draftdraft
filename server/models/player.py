# from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

# Aaron: this is going to end up with us having a circular dependency
# ignore that - you moved it out of app - now it needs to go in its own base probably
db = SQLAlchemy()

class Player(db.Model):
    __tablename__ = 'player'

    player_id = db.Column(db.Integer, primary_key=True)
    player_name_first = db.Column(db.String())
    player_name_last = db.Column(db.String())
    college_team = db.Column(db.String())
    position = db.Column(db.String())

    def __repr__(self):
        return f'Player({self.player_name_first} {self.player_name_last}, {self.college_team} ({self.position}))'

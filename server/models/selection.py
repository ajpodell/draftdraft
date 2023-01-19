# from sqlalchemy import 
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from models.base import db

class Selection(db.Model):
    __tablename__ = 'selection'

    row_id = db.Column(db.Integer, primary_key=True)
    draftdraft_selection = db.Column(db.Integer, db.Sequence('selection_seq'), nullable=False)  # make this draftdraft_selection
    player_id = db.Column(db.Integer(), ForeignKey("player.player_id"))  # add a foreign key to player
    selecting_team_id = db.Column(db.Integer(), ForeignKey("user.user_id"))  # add a foreign key to user

    player = relationship('Player', back_populates="selection")
    team = relationship('User', back_populates='selection')

    
    # def __repr__(self):
    #     return f'Player({self.player_name_first} {self.player_name_last}, {self.college_team} ({self.position}))'

# from sqlalchemy import 

from models.base import db

class Selection(db.Model):
    __tablename__ = 'selection'

    row_id = db.Column(db.Integer, primary_key=True)
    draft_draft_selection = db.Column(db.Integer, db.Sequence('selection_seq'))  # make this draftdraft_selection
    player_name = db.Column(db.String())
    team_name = db.Column(db.String())
    actual_ = db.Column(db.String())

    # def __repr__(self):
    #     return f'Player({self.player_name_first} {self.player_name_last}, {self.college_team} ({self.position}))'

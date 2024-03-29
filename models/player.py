from sqlalchemy.orm import relationship

from models.base import db

class Player(db.Model):
    __tablename__ = 'player'

    player_id = db.Column(db.Integer, primary_key=True)
    player_name_first = db.Column(db.String())
    player_name_last = db.Column(db.String())
    college_team = db.Column(db.String())
    position = db.Column(db.String())

    selection = relationship('Selection', back_populates="player", uselist=False)

    nfl_draft_pick = db.Column(db.Integer())

    @property
    def player_name(self):
        return f'{self.player_name_first} {self.player_name_last}'

    # @hybrid_property
    @property
    def is_selected(self):
        return bool(self.selection)

    def __repr__(self):
        return f'Player({self.player_name_first} {self.player_name_last}, {self.college_team} ({self.position}))'

    @property
    def nfl_draft_pick_formatted(self):
        return self.nfl_draft_pick or '-'


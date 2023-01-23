""" User class. 

This is doubling as a team for now. Once we have a concept of leagues then a mapping of teams makes more sense.
"""
from flask_login import UserMixin
from sqlalchemy.orm import relationship

from models.base import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    is_admin = db.Column(db.Boolean(), default=False)  # better to have some type of enum but this is easier

    def get_id(self):
        return self.user_id

    # Doubling users as "teams" for now. Perhaps in the future will make leagues and teams
    from models import selection
    selections = relationship('Selection', back_populates="team")

    # testing why this is throwing an error
    from models import draft
    pick = relationship('Draft', back_populates="team", uselist=False)

    @property
    def team_score(self):
        """ get the current score"""
        return sum(selection.player.nfl_draft_pick or 0 for selection in self.selections)

    @property
    def team_name(self):
        """ property for team name in case we want to make a display name or multi team option """
        return self.username

    @property
    def team_id(self):
        self.user_id

    @property
    def pick_order(self):
        return self.pick.pick_order


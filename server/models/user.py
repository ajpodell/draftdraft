from flask_login import UserMixin
from sqlalchemy.orm import relationship

from models.base import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    is_admin = db.Column(db.Boolean(), default=False)  # better to have some type of enum but this is easier

    # putting "team name" in here for now. Perhaps in the future will make leagues and teams
    selection = relationship('Selection', back_populates="team")

    def get_id(self):
        return self.user_id

    @property
    def team_name(self):
        """ property for team name in case we want to make a display name or multi team option """
        return self.username

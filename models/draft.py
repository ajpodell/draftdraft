""" this isnt fully thought out - but basically a draft order """
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from models.base import db

class Draft(db.Model):
    __tablename__ = 'draft'

    row_id = db.Column(db.Integer, primary_key=True)

    team_id = db.Column(db.Integer(), ForeignKey("user.user_id"))  # add a foreign key to user
    pick_order = db.Column(db.Integer())

    team = relationship('User', back_populates='pick')

""" this model represents players' individual queues"""
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from models.base import db

class DraftQueue(db.Model):
    __tablename__ = 'draft_queue'
    
    row_id = db.Column(db.Integer, primary_key=True)

    player_id = db.Column(db.Integer(), ForeignKey("player.player_id"))
    team_id = db.Column(db.Integer(), ForeignKey("user.user_id"))
    queue_order = db.Column(db.Integer())
    # order - can we build a table to reorder them?

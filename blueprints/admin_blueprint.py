""" Super user pages. 

admin is pretty light how were handling but thats fine. Also - dont think actually going to build
admin-only for now. Let everyone input scores!
"""

from flask import (
    Blueprint,
    Flask,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required

from models.base import db
from models.player import Player
from models.selection import Selection
from models.user import User

admin = Blueprint('admin', __name__)



# TODO:`reset_draft` - admin only
# randomize players
# remove all the selections
# set selection_seq back to 0

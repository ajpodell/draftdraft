#!/usr/bin/env python
""" Tool to run the db setup command.

Theres probably a cleaner way to do this, but this is what I've got.

Note: all models must be imported for this to work. Not sure if thats always needed, but, again, what all i know so far.
"""

# import sys
# print(sys.path)
# import pdb; pdb.set_trace()

# from the top level - import our app and db
from app import app, db

from models.player import Player # import player, selection
from models.selection import Selection


with app.app_context():
    db.init_app(app)
    db.create_all()

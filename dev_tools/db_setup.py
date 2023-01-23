#!/usr/bin/env python
""" Tool to run the db setup command.

Theres probably a cleaner way to do this, but this is what I've got.

Note: all models must be imported for this to work. Not sure if thats always needed, but, again, what all i know so far.
"""
import app as app_file
from models import (
    base,
    player,
    selection,
    user,
)

app = app_file.create_app()
with app.app_context():
    base.db.init_app(app)
    base.db.create_all()

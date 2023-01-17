# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy

from blueprints import (
    auth_blueprint,
    draft_blueprint,
)
from models.base import db
from models.player import Player
from models.selection import Selection


def create_app(debug=True):
    """ configure our application object. 

    TODO: Right now were just adding blueprints, but could set up debug or configure db here.
          Move the routes to another blueprint so we dont need the global app
    """
    # Flask constructor takes the name of
    # current module (__name__) as argument.
    app = Flask(__name__)

    # aaron going rogue - figure this out
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/draftdraft"

    # sqlalchemy code largely copied from
    # https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
    # this actually has some not great code - should find a new tutorial
    # 
    # app.config.from_object(os.environ['APP_SETTINGS'])
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    if debug:
        # run() method of Flask class runs the application
        # on the local development server.
        # TODO: this should be like an "if debug" type of thing -- 
        app.config['TEMPLATES_AUTO_RELOAD'] = True

    app.register_blueprint(auth_blueprint.auth)
    app.register_blueprint(draft_blueprint.draft)
    return app

def run_app():
    app = create_app()
    app.run(debug=True)

 
# main driver function
if __name__ == '__main__':
    run_app()

# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, redirect, url_for, request, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from blueprints import (
    auth_blueprint,
    draft_blueprint,
)
from models.base import db
from models.draft_queue import DraftQueue
from models.player import Player
from models.selection import Selection
from models.user import User


def create_app():
    """ configure our application object. 

    TODO: Right now were just adding blueprints, but could set up debug or configure db here.
          Move the routes to another blueprint so we dont need the global app
    """
    # Flask constructor takes the name of
    # current module (__name__) as argument.
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # sqlalchemy code largely copied from
    # https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
    # this actually has some not great code - should find a new tutorial
    # 
    # app.config.from_object(os.environ['APP_SETTINGS'])
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # wire up flask migrations
    migrate = Migrate(app, db)

    if app.config.get('DEBUG'):
        # run() method of Flask class runs the application
        # on the local development server.
        # TODO: this should be like an "if debug" type of thing -- 
        app.secret_key = 'super_secret_key'

    # configure blueprints
    app.register_blueprint(auth_blueprint.auth)
    app.register_blueprint(draft_blueprint.draft)

    # set up the flask-login things
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    return app


def run_app():
    app = create_app()
    app.run(debug=app.config.get('DEBUG'))


# main driver function
if __name__ == '__main__':
    run_app()

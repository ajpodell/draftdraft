""" The main blueprint file for now."""

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

draft = Blueprint('draft', __name__)

@draft.before_request
def check_valid_login():
    """ Detect if user is logged in as the default - basically equivalent to `@login_required`
        TODO: force user to set their team name
    """
    # ensure user is logged in
    login_valid = current_user.is_authenticated
    if (request.endpoint and 
        'static' not in request.endpoint and 
        not login_valid and 
        not getattr(draft.view_functions.get(request.endpoint, {}), 'is_public', False) ) :
        return render_template('login.html', next=request.endpoint)

def public_endpoint(function):
    """ decorator to make public -- probably want to functools wraps this """
    function.is_public = True
    return function

 
@draft.route('/home')  # maybe theres a better way to do url_for('/')
@draft.route('/')
def home():
    # kind of want to put home in a dedicated "make pick" page - but thats a later problem
    #TODO: have an "is_picked" property - can probably do this as a hybrid python thing on the model 
    # looking at the draft
    players = db.session.query(Player).all()
    return render_template('app.html', players=players)

@draft.route('/players')
def players():
    players = db.session.query(Player).all()
    return list(player.__repr__() for player in players)

@draft.route('/add_selection', methods=['POST'])
def add_selection():
    return {}

    # THIS IS BROKEN SINCE YOU CHANGED TABLES TO USE FOREIGN REFERENCE TO THE PLAYER VALUES NOWQ
    form = request.form
    selection = Selection(player_name=form['player_name'], team_name=form['team_name'])
    db.session.add(selection)
    db.session.commit()
    return {}

@draft.route('/draft')  # would be cool to have a "league" template var
# @login_required
def view_draft():
    # TODO: generally not a fan of passing around sqlalchemy objects --- but it is pretty convenient so :shrug:
    all_picks = db.session.query(Selection).all()

    # get all teams
    teams = db.session.query(User).all()
    print(teams[0].selections)


    return render_template('draft.html', selections=all_picks, teams=teams)

@draft.route('/selected_row', methods=['POST'])
def selected_row():
    """ this can maybe just be the same 'pick' endpoint' if i figure out how this works"""
    form = request.form
    selected_player_id = form['player_id']
    user_id = current_user.user_id

    # TODO: add some sort of protection that its actually the user's turn
    selection = Selection(player_id=selected_player_id, selecting_team_id=user_id)
    db.session.add(selection)
    db.session.commit()
    return redirect(url_for('draft.view_draft'))


# TODO:`reset_draft` - admin only
# randomize players
# remove all the selections
# set selection_seq back to 0

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
from models.selection import Selection

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

def render_home():
    """ render the home page.
        Centralizing this in case want to call it in more places and also if move the homepage.
    """
    return render_template('app.html')
 
@draft.route('/home')  # maybe theres a better way to do url_for('/')
@draft.route('/')
# @login_required
def home():
    return render_home()

@draft.route('/players')
def players():
    players = db.session.query(Player).all()
    return list(player.__repr__() for player in players)

@draft.route('/add_selection', methods=['POST'])
def add_selection():
    form = request.form
    selection = Selection(player_name=form['player_name'], team_name=form['team_name'])
    db.session.add(selection)
    db.session.commit()
    return {}

@draft.route('/draft')  # would be cool to have a "league" template var
# @login_required
def view_draft():
    all_picks = db.session.query(Selection).all()
    # make the object returnable. 
    # can probably use jsonify or put this in the object
    # selections = [[s.draft_draft_selection, s.team_name, s.player_name] for s in all_picks]
    return render_template('draft.html', selections=all_picks)

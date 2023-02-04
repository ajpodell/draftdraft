""" The main blueprint file for now."""
import random

from flask import (
    Blueprint,
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from sqlalchemy import desc, asc, nulls_last

from models.base import db
from models.draft import Draft
from models.draft_queue import DraftQueue
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
            not getattr(draft.view_functions.get(request.endpoint, {}), 'is_public', False)):
        return render_template('login.html', next=request.endpoint)


def public_endpoint(function):
    """ decorator to make public -- probably want to functools wraps this """
    function.is_public = True
    return function


def generate_leaderboard(leaderboard_type):
    differential_column_label = 'pick_differential'
    sort_dir = asc(differential_column_label) if leaderboard_type == "worst" else desc(differential_column_label)

    rows = (
        db.session.query(
            Player.player_name_first,
            Player.player_name_last,
            User.username,
            (Selection.draftdraft_selection - Player.nfl_draft_pick).label(differential_column_label)
        )
        .join(Selection, Selection.player_id == Player.player_id)
        .join(User, Selection.selecting_team_id == User.user_id)
        .order_by(nulls_last(sort_dir))
        .limit(3)
        .all()
    )

    return rows

def next_up():
    """ returns team id of the next team up"""
    last_pick = db.session.query(Selection).order_by(Selection.draftdraft_selection.desc()).first()
    if last_pick is None:
        next_pick = 0
    else:
        next_pick = last_pick.draftdraft_selection

    all_teams = db.session.query(User).all()
    total_teams = len(all_teams)
    next_pick = (next_pick % len(all_teams)) + 1

    # if no draft has been set yet then return empty for now.
    # the below code assumes if any team has a pick all teams have a piack
    if not all_teams or not all_teams[0].pick:
        return None

    return next(team for team in all_teams if team.pick.pick_order == next_pick)


@draft.route('/home')  # maybe theres a better way to do url_for('/')
@draft.route('/')
def home():
    """ This is the main page of the app. As of now it shows the draft order and board."""
    # kind of want to put home in a dedicated "make pick" page - but thats a later problem
    pick_order = db.session.query(Draft).order_by(Draft.pick_order)

    next_pick = next_up()

    player_queue = db.session.query(Player).join(DraftQueue, DraftQueue.player_id == Player.player_id).filter_by(team_id=current_user.user_id).order_by(DraftQueue.queue_order, DraftQueue.row_id).all()
    print(player_queue)

    return render_template('draft_page.html', players=players(), pick_order=pick_order, next_pick=next_pick, playerQueue=player_queue)

@draft.route('/add_to_queue', methods=['POST'])
def add_to_queue():
    form = request.form
    db.session.add(
        DraftQueue(
            player_id=form['player_id'],
            team_id=current_user.user_id,
        )
    )
    db.session.commit()
    return redirect(url_for('draft.home'))


def players():
    # TODO: have an "is_picked" property - can probably do this as a hybrid python thing on the model
    # looking at the draft
    players = db.session.query(Player).order_by(Player.player_id).all()
    return players


@draft.route('/players', methods=['POST'])
def add_player():
    form = request.form
    player = Player(player_name_first=form['player_name_first'],
                    player_name_last=form['player_name_last'],
                    college_team=form['college_team'],
                    position=form['position'])

    db.session.add(player)
    db.session.commit()

    return render_template('admin_tools.html', players=players())


@draft.route('/add_selection', methods=['POST'])
def add_selection():
    """ todo: just delete this?"""
    return {}

    # THIS IS BROKEN SINCE YOU CHANGED TABLES TO USE FOREIGN REFERENCE TO THE PLAYER VALUES NOWQ
    form = request.form
    selection = Selection(player_name=form['player_name'], team_name=form['team_name'])
    db.session.add(selection)
    db.session.commit()
    return {}


@draft.route('/draft')  # would be cool to have a "league" template var
def view_draft():
    # TODO: generally not a fan of passing around sqlalchemy objects --- but it is pretty convenient so :shrug:
    all_picks = db.session.query(Selection).all()

    # get all teams
    teams = db.session.query(User).all()

    team_standings = User.standings(db.session)
    return render_template('draft.html',
                           selections=all_picks,
                           teams=teams,
                           best_selections=generate_leaderboard('best'),
                           worst_selections=generate_leaderboard('worst'),
                           standings=team_standings)


@draft.route('/draft_player', methods=['POST'])
def draft_player():
    """ this can maybe just be the same 'pick' endpoint' if i figure out how this works"""
    form = request.form
    selected_player_id = form['player_id']
    user_id = current_user.user_id

    # TODO: add some sort of protection that its actually the user's turn
    next_pick = next_up()
    if next_pick is None:
        flash('Draft order not yet set', 'error')
        return redirect(url_for('draft.home'))

    # picked = db.session
    picked = Selection.query.filter_by(player_id=selected_player_id).one_or_none()
    if (picked):
        flash('Player already selected', 'error')
        return redirect(url_for('draft.home'))

    if not current_user.user_id == next_pick.user_id and not current_user.is_admin:
        flash('Not your pick', 'error')
        return redirect(url_for('draft.home'))

    selection = Selection(player_id=selected_player_id,
                          selecting_team_id=next_pick.user_id)  # wasnt working with team_id
    db.session.add(selection)
    db.session.commit()
    return redirect(url_for('draft.view_draft'))


@draft.route('/score_players.html')
def score_players():
    """ as of yet unused view for a dedicated scoring """
    return render_template('score_players.html')


@draft.route('/reset_draft', methods=['POST'])
def reset_draft():
    if not current_user.is_authenticated or not current_user.is_admin:
        return

    # delete all selections and the draft order
    db.session.execute(' TRUNCATE table public.selection; TRUNCATE table public.draft;')
    db.session.execute('ALTER SEQUENCE selection_seq RESTART WITH 1')
    db.session.commit()

    teams = db.session.query(User).all()
    random.shuffle(teams)
    for pick, team in enumerate(teams, start=1):
        # this didnt work with team_id. maybe need hybridy_property?
        db.session.add(Draft(team_id=team.user_id, pick_order=pick))
        db.session.commit()

    return redirect(url_for('draft.home'))


@draft.route('/score_player', methods=['POST'])
def score_player():
    """ score an invidual player """
    player_id = request.form['player_id']
    nfl_draft_pick = request.form['nfl_draft_pick']

    try:
        int(nfl_draft_pick)  # can raise if None (maybe others)
    except:
        return redirect(url_for('draft.home'))

    if not int(nfl_draft_pick):
        # FLASH
        return redirect(url_for('draft.home'))  # maybe should bring back render_home()
    print('updating')
    db.session.query(Player).filter_by(player_id=player_id).update({Player.nfl_draft_pick: nfl_draft_pick})
    db.session.commit()
    return redirect(url_for('draft.home'))


@draft.route('/admin_tools')
def admin_tools():
    return render_template('admin_tools.html', players=players())

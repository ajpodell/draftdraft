""" The main blueprint file for now."""

from flask import Blueprint, render_template
from flask import Flask, redirect, url_for, request

draft = Blueprint('draft', __name__)

# can you have Flask stuff floating? 
def render_home():
    """ render the home page.
        Centralizing this in case want to call it in more places and also if move the homepage.
    """
    return render_template('app.html')
 
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@draft.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return render_home()

@draft.route('/success/<name>')
def success(name):
    return 'welcome %s' % name
 
 
@draft.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['user_name']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('user_name')
        return redirect(url_for('success', name=user or 'Uh oh'))

@draft.route('/players')
def players():
    players = db.session.query(Player).all()
    return list(player.__repr__() for player in players)

@draft.route('/add_selection', methods=['POST'])
def add_selection():
    print(request.form)
    # return redirect(url_for(''))
    # return render_template('app.html')

    form = request.form
    selection = Selection(player_name=form['player_name'], team_name=form['team_name'])
    print(selection)
    db.session.add(selection)
    db.session.commit()
    return {}


@draft.route('/draft')  # would be cool to have a "league" template var
def view_draft():
    all_picks = db.session.query(Selection).all()
    # make the object returnable. 
    # can probably use jsonify or put this in the object
    # selections = [[s.draft_draft_selection, s.team_name, s.player_name] for s in all_picks]
    return render_template('draft.html', selections=all_picks)

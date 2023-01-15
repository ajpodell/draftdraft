# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy

from models.base import db
from models.player import Player
from models.selection import Selection

 
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



# can you have Flask stuff floating? 
def render_home():
    """ render the home page.
        Centralizing this in case want to call it in more places and also if move the homepage.
    """
    return render_template('index.html')
 
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return render_home()

@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name
 
 
@app.route('/login', methods=['POST', 'GET'])
def login():
    print('hi')
    if request.method == 'POST':
        user = request.form['user_name']
        print(user)
        return redirect(url_for('success', name=user))
    else:
        print('hi')
        user = request.args.get('user_name')
        return redirect(url_for('success', name=user))

@app.route('/players')
def players():
    players = db.session.query(Player).all()
    return list(player.__repr__() for player in players)

@app.route('/add_selection', methods=['POST'])
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

@app.route('/draft')  # would be cool to have a "league" template var
def view_draft():
    all_picks = db.session.query(Selection).all()
    # make the object returnable. 
    # can probably use jsonify or put this in the object
    # selections = [[s.draft_draft_selection, s.team_name, s.player_name] for s in all_picks]
    return render_template('draft.html', selections=all_picks)
 
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    # TODO: this should be like an "if debug" type of thing -- 
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    print('testing')

    app.run(debug=True)

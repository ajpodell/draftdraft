# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

from models.player import db, Player

 
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


 
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    print('this?')
    return 'Hey Greg and Dan! Let our Draft Draft Development begin!'

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
 
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)

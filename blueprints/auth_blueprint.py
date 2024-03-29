""" Auth related activity (login/logou) """
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from models.base import db
from models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/signup')
def signup():
    return render_template('signup.html')


def create_user(username, password):
    """ utility for creating the user so can make a little utility for adding test data"""
    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()


@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    username = request.form.get('username')
    password = request.form.get('password')

    # check if username already exists
    user = User.query.filter_by(username=username).one_or_none()
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('username already exists')
        return redirect(url_for('auth.signup'))

    if not username or not password:
        flash('must input both username and password')
        return redirect(url_for('auth.signup'))

    create_user(username, password)

    return redirect(url_for('auth.login'))

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('draft.index'))

    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember-me') else False

    user = User.query.filter_by(username=username).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('draft.index'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


from flask import Blueprint, render_template, redirect, url_for, request, flash, session, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from flask_session import Session
from .models import User
from . import db
from . import *
from .cookies import *
from datetime import datetime, timedelta

expires=datetime.now()
expires=expires+timedelta(days=90)

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/login0',methods=["POST"])
def login_post():
    session['email'] = request.form.get('email')
    session['password'] = request.form.get('password')
    remember = True if request.form.get('remember') else False
    email=session['email']
    password=session['password']
    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    res= make_response(redirect('/profile'))
    res.set_cookie("email",email, expires=expires)
    return res


@auth.route('/signup',methods=["POST"])
def signup_post():
    session['email']=request.form.get("email")
    session['name']=request.form.get("name")
    session['password_0']=request.form.get("password_1")
    session['password_1']=request.form.get("password_2")
    email=session['email']
    name=session['name']
    password_0=session['password_0']
    password_1=session['password_1']
    if password_0==password_1:
        password=password_1
    else:
        flash("Two password are not equal")
        return render_template("signup.html")
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash("Email address already exists")
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
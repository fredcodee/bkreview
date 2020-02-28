from flask import Blueprint, render_template, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from . models import User
from . import db

auth = Blueprint('auth', __name__)

#check login verification
@auth.route('/login', methods=["GET", "POST"])
def login():
  if request.method == "POST":
    username = request.form.get('username')
    password = request.form.get('password')

    #check user details if its  correct
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
      flash('incorrect email or password')
      return(redirect(url_for('auth.login')))

    login_user(user)
    return(redirect(url_for('main.home')))
  else:
    return(render_template("login.html"))


#register a user
@auth.route('/signup', methods=["GET", "POST"])
def signup():
  if request.method == "POST":
    email = request.form.get('email')
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')

    # Ensure required details  was submitted
    if not email or not name or not password or not username:
      flash("must provide all required details")
      return(redirect(url_for('auth.signup')))
    if len(password) < 4:
      flash("password too weak choose a stronger option")
      return(redirect(url_for('auth.signup')))

    #check if user exits in database
    user = User.query.filter_by(email=email).first()
    if user:
      flash('sorry this email address is already registered')
      return(redirect(url_for('auth.signup')))
    
    usern = User.query.filter_by(username=username).first()
    if usern:
      flash('sorry this username is already taken')
      return(redirect(url_for('auth.signup')))

    else:
      #registring new user
      new_user = User(email=email, username=username,
                      password=generate_password_hash(password, method='sha256'))

      db.session.add(new_user)
      db.session.commit()
      return(redirect(url_for('auth.login')))
  else:
    return(render_template("signup.html"))

#logout
@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return(redirect(url_for('main.home')))

import requests
from flask import Flask, session, Blueprint, redirect, render_template, request, flash, jsonify
from flask_login import LoginManager, login_required, current_user
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
'''from models import User, Books, Reviews'''


import requests
import json
import json

app = Flask(__name__)


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(
    "postgres://cajflrevfbywfx:3259245e928346a9eb88e48cb28d93c7e369b044ce6adde32ee7cda98af2019c@ec2-184-72-235-80.compute-1.amazonaws.com:5432/dbrbakv104v2pv")
db = scoped_session(sessionmaker(bind=engine))

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return(User.query.get(int(user_id)))

@app.route("/")
def index():
    return(render_template("base.html"))

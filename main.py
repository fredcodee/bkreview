from flask import Flask, Blueprint, redirect, render_template, request, flash, jsonify
from flask_login import LoginManager, login_required, current_user
from . models import User, Books, Review
import requests
import json
import json

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return(render_template("base.html"))

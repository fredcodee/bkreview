from flask import Flask, Blueprint, redirect, render_template, request, flash, jsonify,url_for
from flask_login import LoginManager, login_required, current_user
from . models import User, Books, Review
import requests
import json


main = Blueprint('main', __name__)

@main.route("/")
def home():
    return(render_template("base.html"))


@main.route("/search", methods=['POST'])
def search():
    get_book = request.form.get("book").title()

  #check if book details was provided
    if get_book:
        try:
            from sqlalchemy import or_
            books = Books.query.filter(or_(Books.title==get_book, Books.auther==get_book)).all()
            return(render_template("booklist.html", books=books))
        except:
            flash("error in db code")
            return(redirect(url_for("main.home")))
    else:
        flash("sorry you must provide a book details")
        return(redirect(url_for("main.home")))

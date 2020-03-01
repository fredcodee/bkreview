from flask import Flask, Blueprint, redirect, render_template, request, flash, jsonify,url_for
from flask_login import LoginManager, login_required, current_user
from . models import User, Books, Review
from . import db
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
        from sqlalchemy import or_
        books = Books.query.filter(or_(Books.isbn== get_book, Books.author == get_book, Books.title == get_book)).all()
        if books:
            return(render_template("booklist.html", books=books))
        else:
            flash("we can't find books with that description.")
            return(redirect(url_for("main.home")))
    else:
        flash("sorry you must provide a book details")
        return(redirect(url_for("main.home")))


@main.route("/book/<isbn>")
def book(isbn):
    book_id = Books.query.filter_by(isbn=isbn).first()

    """GOODREADS"""
    #get api key
    key = "82F9vHtuZ1UxuDWQHifAA"
    res = requests.get("https://www.goodreads.com/book/review_counts.json",params={"key": key, "isbns": isbn})
    
    #parse json to dict
    a = res.json()
    bd = a['books'][0]

    # Fetch book reviews
    book_reviews = Review.query.filter_by(book_isbn=isbn).all()
    if len(book_reviews) == 0:
        check=False
    else:
        check=True


    return(render_template('bookpage.html', title=book_id.title, author=book_id.author, year=book_id.year, isbn=bd['isbn'], av=bd['average_rating'], wrc=bd['work_ratings_count'], reviews=book_reviews, check=check))



@main.route("/book/<isbn>", methods=['POST'])
@login_required
def book_post(isbn):
    review = request.form.get('comment')

    if review:
        save_review=Review(book_isbn=isbn,comment=review, feedback=current_user)
        db.session.add(save_review)
        db.session.commit()

        flash("Review uploaded successfully")
        return(redirect(url_for('main.book', isbn=isbn)))
    else:
        flash("please leave a review")
        return(redirect(url_for('main.book', isbn=isbn)))


@main.route("/<username>")
@login_required
def profile(username):
    #get user reviews
    user_reviews = Review.query.all()
    t = []
    for info in user_reviews:
        if info.feedback.email == current_user.email:
            t.append(info)
    return(render_template("profile.html", info=t))

#delete reviews
@main.route("/delete/<id>")
@login_required
def delete(id):
    get_review = Review.query.filter_by(id=int(id)).first()
    db.session.delete(get_review)
    db.session.commit()
    return redirect(url_for('main.profile', username= current_user.username))

from flask import Flask, Blueprint, redirect, render_template, request, flash, jsonify,url_for,abort
from flask_login import LoginManager, login_required, current_user
from . models import User, Books, Review
from . import db
import requests
import json


main = Blueprint('main', __name__)

#goodreads api key
key = "82F9vHtuZ1UxuDWQHifAA"


@main.route("/")
def home():
    #home suggestions
    def getsug_id():
        import random
        sug_id = []
        for i in range(3):
            n = random.randrange(1, 5000)
            sug_id.append(n)
        return(sug_id)

    suggestions=[]
    for suglist in getsug_id():
        n= Books.query.filter_by(id=int(suglist)).first()
        suggestions.append(n)


    return(render_template("base.html", suggestions=suggestions))


@main.route("/search", methods=['POST'])
def search():
    get_book = request.form.get("book").title()

    #check if book details was provided
    if get_book:
        from sqlalchemy import or_
        books = Books.query.filter(or_(Books.isbn== get_book, Books.author == get_book, Books.title == get_book)).all()
        if books:
            return(render_template("booklist.html", books=books, search=get_book))
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

    context={ "title":book_id.title,
     "author":book_id.author,
     "year":book_id.year,
     "isbn":bd['isbn'],
     "av":bd['average_rating'],
     "wrc":bd['work_ratings_count'],
     "reviews":book_reviews,
     "check":check
    }
    return(render_template('bookpage.html', **context))



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
    get_user = User.query.filter_by(username=username).first()
    if not get_user or username != current_user.username:
        abort(404)
    #get user reviews
    user_reviews = Review.query.all()
    t = []
    for info in user_reviews:
        if info.feedback.email == current_user.email:
            t.append(info)
    count=len(t)
    return(render_template("profile.html", info=t, count=count))

#delete reviews
@main.route("/delete/<id>")
@login_required
def delete(id):
    get_review = Review.query.filter_by(id=int(id)).first()
    db.session.delete(get_review)
    db.session.commit()
    return redirect(url_for('main.profile', username= current_user.username))

#error handling
@main.errorhandler(404)
def error404(error):
  return(render_template('404.html'), 404)

#API Access
@main.route("/api/<isbn>")
def bkreviews_api(isbn):
    book_isbn = Books.query.filter_by(isbn=isbn).first()

    if not book_isbn:
        return(render_template('404.html'), 404)
    
    """GOODREADS"""
    r = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": isbn})
    a = r.json()
    return(jsonify(a))
    

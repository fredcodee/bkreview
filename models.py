from flask_login import UserMixin
from datetime import datetime
from . import db


class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(100))
  reviews = db.relationship('Review', backref='comment', lazy=True)


class Books(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  isbn = db.Column(db.String)
  title = db.Column(db.String)
  author = db.Column(db.String)
  year = db.Column(db.String)


class Review(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  dateposted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  book_isbn = db.Column(db.String)
  comment = db.Column(db.String)
  


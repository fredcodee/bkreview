import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://cajflrevfbywfx:3259245e928346a9eb88e48cb28d93c7e369b044ce6adde32ee7cda98af2019c@ec2-184-72-235-80.compute-1.amazonaws.com:5432/dbrbakv104v2pv")
db = scoped_session(sessionmaker(bind=engine))


def main():
  f = open("books.csv")
  reader = csv.reader(f)
  for isbn, title, author, year in reader:
    db.execute("INSERT INTO Books (isbn,title,author,year) VALUES (:isbn, :title, :author, :year)",{"isbn": isbn, "title": title, "author": author, "year": year})
  
  db.commit()


main()
print("done")

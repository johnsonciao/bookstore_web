# -*- coding: utf-8 -*-

from database import Author, Book
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_whooshalchemy as wa

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  #whooshalachemy才知道
app.config['DEBUG'] = True
app.config['WHOOSH_BASE']='whoosh'

db = SQLAlchemy(app)

db.create_all();
wa.whoosh_index(app, Book)

# Book for Alexis Angel
author1 = Author(name="Alexis Angel")
db.session.add(author1)
db.session.commit()


book1 = Book(name="Java Usage", description="how to use java",
                     price="9.99", author=author1)
db.session.add(book1)
db.session.commit()

book2 = Book(name="C++ Usage", description="how to use c++",
                     price="5.50", author=author1)
db.session.add(book2)
db.session.commit()

book3 = Book(name="Chinese Collection", description="chinese poetry collection from Ming dynasty",
                     price="3.99", author=author1)
db.session.add(book3)
db.session.commit()

book4 = Book(name="TOEFL? What's it?", description="how to beat TOEFL in 2 months",
                     price="15.99", author=author1)
db.session.add(book4)
db.session.commit()

book5 = Book(name="TOEFL Vocabulary 10000", description="words you need to know to beat TOEFL",
                     price="10.99", author=author1)
db.session.add(book5)
db.session.commit()

book6 = Book(name="Python Usage", description="how to use python",
                     price="8.55", author=author1)
db.session.add(book6)
db.session.commit()


# Book for Mark Lutz
author2 = Author(name="Mark Lutz")

db.session.add(author2)
db.session.commit()


book1 = Book(name="Learning Python, 5th Edition", description="grasp python easily",
                     price="7.99", author=author2)
db.session.add(book1)
db.session.commit()

book2 = Book(
    name="Fluent Python", description=" Clear, Concise, and Effective Programming", price="18", author=author2)
db.session.add(book2)
db.session.commit()

book3 = Book(name="Java: A Beginner's Guide, Sixth Edition", description="A Complete Beginners Guide To Java Programming Mastery ",
                     price="15.50", author=author2)
db.session.add(book3)
db.session.commit()

book4 = Book(name="Head First Java, 2nd Edition", description="Learn Java in One Day and Learn It Well",
                     price="12.90", author=author2)
db.session.add(book4)
db.session.commit()

book5 = Book(name="Java Programming: Your Step by Step Guide to Easily Learn Java in 7 Days", description="Beginning Programming with Java For Dummies",
                     price="14.99", author=author2)
db.session.add(book5)
db.session.commit()


# Book for Al Sweigart
author3 = Author(name="Al Sweigart")
db.session.add(author3)
db.session.commit()


book1 = Book(name="Core Java, Volume II--Advanced Features", description="Lambdas, Streams, and functional-style programming",
                     price="8.99", author=author3)
db.session.add(book1)
db.session.commit()

book2 = Book(name="Automate the Boring Stuff with Python: Practical Programming for Total Beginners", description="Python Pocket Reference: Python In Your Pocket ",
                     price="6.50", author=author3)
db.session.add(book2)
db.session.commit()

book3 = Book(name="English Made Easy Volume One:", description=" A New ESL Approach: Learning English Through Pictures",
                     price="9.95", author=author3)
db.session.add(book3)
db.session.commit()

book4 = Book(name="Prisoners of Geography", description="Ten Maps That Explain Everything About the World",
                     price="6.99", author=author3)
db.session.add(book4)
db.session.commit()

book5 = Book(name="Geography of the World", description="Geography: A Visual Encyclopedia",
                     price="9.50", author=author3)
db.session.add(book5)
db.session.commit()


# Book for Paul Jones
author4 = Author(name="Paul Jones")
db.session.add(author4)
db.session.commit()


book1 = Book(name="Python: The Fundamentals Of Python Programming", description=" A Complete Beginners Guide To Python Mastery.",
                     price="10.99", author=author4)
db.session.add(book1)
db.session.commit()

book2 = Book(name="Java in 24 Hours", description="OCA / OCP Java SE 8 Programmer Certification ",
                     price="10.99", author=author4)
db.session.add(book2)
db.session.commit()

book3 = Book(name="Honey Boba Shaved Snow", description="Intro to Java Programming, Comprehensive Version",
                     price="14.50", author=author4)
db.session.add(book3)
db.session.commit()

book4 = Book(name="Core Java for the Impatient", description="Golden fried cauliflower florets in a midly spiced soya,garlic sauce cooked with fresh cilantro, celery, chilies,ginger & green onions",
                     price="6.95", author=author4)
db.session.add(book4)
db.session.commit()

book5 = Book(name="Everything You Need to Ace Math in One Big Fat Notebook", description=" The Mathemagician's Guide to Lightning Calculation",
                     price="7.95", author=author4)
db.session.add(book5)
db.session.commit()
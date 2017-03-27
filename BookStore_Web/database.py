# -*- coding: utf-8 -*-


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_whooshalchemy as wa
from flask_login import UserMixin

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG'] = True
app.config['WHOOSH_BASE']='whoosh'

db = SQLAlchemy(app)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    books = db.relationship('Book', backref='author',cascade="all, delete-orphan", lazy='dynamic')
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Book(db.Model):
    __searchable__ = ['name','description']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(250))
    price = db.Column(db.String(8))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
        }


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

db.create_all();
wa.whoosh_index(app, Book)

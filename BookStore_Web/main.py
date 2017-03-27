from database import Author, Book, User
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
import flask_whooshalchemy as wa
from sqlalchemy.sql import func
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'utofunisgood!'
app.config['DEBUG'] = True
app.config['WHOOSH_BASE'] = 'whoosh'
Bootstrap(app)
db = SQLAlchemy(app)
wa.whoosh_index(app, Book)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)])


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Home page before logging in
@app.route('/', methods=['GET', 'POST'])
def index_1():
    authors = Author.query.all()
    books = Book.query.all()
    return render_template('index_1.html', authors=authors, books=books)


# Home page after logging in
@app.route('/permit', methods=['GET', 'POST'])
@login_required
def index_2():
    authors = Author.query.all()
    books = Book.query.all()
    return render_template('index_2.html', authors=authors, books=books, name=current_user.username)


# Sign-up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(' Congratulation! Please input your username and password again! ')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


# Log-in page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index_2'))
        flash('Username and Password not ACCEPTED')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


# Log-out page
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index_1'))


# Authors in JSON form
@app.route('/author/JSON')
@login_required
def author_json():
    authors = db.session.query(Author).all()
    return jsonify(authors=[r.serialize for r in authors])

# Books in JSON form
@app.route('/book/JSON')
@login_required
def book_json():
    books = db.session.query(Book).all()
    return jsonify(books=[r.serialize for r in books])


# Author result of searching by Author ID:
@app.route('/author/', methods=['GET', 'POST'])
@login_required
def show_author():
    if request.method == 'POST':
        author_id = request.form['author_id']
        qry = db.session.query(func.max(Author.id).label("max_score"),
                               func.min(Author.id).label("min_score"),
                               )
        res = qry.one()
        try:
            author_id = int(author_id)
        except ValueError:
            author_id = -1
        max_id = int(res.max_score)
        min_id = int(res.min_score)
        if author_id > max_id or author_id < min_id:
            flash('Author ID not existing')
            return redirect(url_for('index_2'))
        else:
            return redirect(url_for('show_book', author_id=author_id))
    else:
        authors = Author.query.all()
        books = Book.query.all()
        return render_template('index_2.html',authors=authors, books=books )


# Book result of searching by keyword:
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        books = Book.query.whoosh_search(request.form['query']).all()
        return render_template('search.html', books=books)
    else:
        return render_template('search.html')


# Show Author's book list
@app.route('/author/<int:author_id>/')
@app.route('/author/<int:author_id>/book/')
@login_required
def show_book(author_id):
    author = db.session.query(Author).filter_by(id=author_id).one()
    books = db.session.query(Book).filter_by(
        author_id=author_id).all()
    return render_template('book.html', books=books, author=author)


# Create a new author
@app.route('/author/new/', methods=['GET', 'POST'])
@login_required
def new_author():
    authors = Author.query.all()
    if request.method == 'POST':
        newAuthor = Author(name=request.form['name'])
        db.session.add(newAuthor)
        db.session.commit()
        return redirect(url_for('index_2'))
    else:
        return render_template('newAuthor.html', authors=authors)


# Edit existing author
@app.route('/author/<int:author_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_author(author_id):
    editedAuthor = db.session.query(
        Author).filter_by(id=author_id).one()
    books = db.session.query(Book).filter_by(
        author_id=author_id).all()
    if request.method == 'POST':
        if request.form['name']:
            editedAuthor.name = request.form['name']
            db.session.add(editedAuthor)
            db.session.commit()
            return redirect(url_for('index_2'))
    else:
        return render_template(
            'editAuthor.html', books=books, author=editedAuthor)


# Delete author
@app.route('/author/<int:author_id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_author(author_id):
    authorDeleted = db.session.query(
        Author).filter_by(id=author_id).one()
    booksDeleted = authorDeleted.books.all()
    if request.method == 'POST':
        db.session.delete(authorDeleted)
        db.session.commit()
        for book in booksDeleted:
            print "starttttt"
            db.session.delete(book)
            db.session.commit()
        return redirect(
            url_for('index_2'))
    else:
        print "starttttt"
        return render_template(
            'deleteAuthor.html', booksDeleted=booksDeleted, authorDeleted=authorDeleted)


# Add book to author (done)
@app.route(
    '/author/<int:author_id>/book/new/', methods=['GET', 'POST'])
@login_required
def new_book(author_id):
    author = db.session.query(Author).filter_by(id=author_id).first()
    books = db.session.query(Book).filter_by(author_id=author_id).all()
    if request.method == 'POST':
        newBook = Book(name=request.form['name'], description=request.form[
            'description'], price=request.form['price'], author_id=author_id)
        db.session.add(newBook)
        db.session.commit()
        return redirect(url_for('index_2'))
    else:
        return render_template('newBook.html', books= books, author_id=author_id, author=author)


# Edit Author's existing books
@app.route('/author/<int:author_id>/book/<int:book_id>/edit',
           methods=['GET', 'POST'])
@login_required
def edit_book(author_id, book_id):
    author = db.session.query(Author).filter_by(id=author_id).first()
    editedBook = db.session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedBook.name = request.form['name']
        if request.form['description']:
            editedBook.description = request.form['name']
        if request.form['price']:
            editedBook.price = request.form['price']
        db.session.add(editedBook)
        db.session.commit()
        return redirect(url_for('index_2'))
    else:

        return render_template(
            'editBook.html', author_id=author_id, author = author, book_id=book_id, book=editedBook)


# Delete book
@app.route('/author/<int:author_id>/book/<int:book_id>/delete',
           methods=['GET', 'POST'])
@login_required
def delete_book(author_id, book_id):
    bookDeleted = db.session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        db.session.delete(bookDeleted)
        db.session.commit()
        return redirect(url_for('show_book', author_id=author_id))
    else:
        return render_template('deleteBook.html', book=bookDeleted)


if __name__ == '__main__':
    app.debug = True
    app.run()
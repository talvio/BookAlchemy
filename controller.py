from flask import abort, jsonify, redirect, render_template, request, send_from_directory, url_for
from sqlalchemy import or_
import data_models
from datetime import datetime
from data_models import Author, Book, db

LIBRARY_SERVER = "http://127.0.0.1:5002/"

def validate_date(date_string):
    """ Validate that a date in a string format is a valid date in the format yyyy-mm-dd """
    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d").date()
        return date_obj
    except ValueError:
        return None

def send_favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

def home():
    """
    Show the Library Lobby aka home screen
    :return:
    """
    results = (
        db.session.query(Author, Book)
        .join(Book, Author.author_id == Book.author_id)
        .order_by(Book.title)
        .all()
    )
    return render_template(
        'home.html',
        results=results,
        query_string=""
    )

def show_book(book_id=None, book=None, author=None):
    if book is None:
        if book_id is None:
            return "I need more information to find the book"
        book = Book.query.filter_by(book_id=book_id).first()
    if book is None:
        abort(404)

    if author is None:
        author = Author.query.filter_by(author_id=book.author_id).first()
    try:
        rating = int(book.rating)
    except ValueError:
        rating = 0
    return render_template('show_book.html',
            book=book,
            rating=rating,
            author=author
    )


def edit_book(book_id):
    """ Edit the book. """
    book = Book.query.filter_by(book_id=book_id).first()
    if book is None:
        abort(404)
    author = Author.query.filter_by(author_id=book.author_id).first()
    if author is None:
        abort(500)
    return render_template('edit_book.html', book=book, author=author)


def update_book(book_id=None):
    if book_id is None:
        book_id = request.form.get('book_id', 0)
    book = Book.query.get(book_id)
    author_id = request.form.get('author_id', book.author_id)
    author = Author.query.get(author_id)
    print(author_id, book_id)
    print(author, book)
    if author is None or book is None:
        abort(404)
    if request.method == 'POST' or request.method == 'PUT':
        book.title = request.form.get('title', book.title)
        book.author_id = request.form.get('author_id', book.author_id)
        book.isbn = request.form.get('isbn', book.isbn)
        book.publication_year = request.form.get('publication_year', book.publication_year)
        book.rating = request.form.get('rating', book.rating)
        book.summary = request.form.get('summary', book.summary)
        data_models.update_database()
        return redirect(url_for('show_book', book_id=book.book_id))
    abort(405)


def show_author(author=None, author_id=None):
    if author is None:
        if author_id is None:
            return "No author selected"
        else:
            author = Author.query.get(author_id)
    books_from_writer = data_models.Book.query.filter(data_models.Book.author_id == author_id).all(),
    print(books_from_writer)
    return render_template('show_author.html',
        name=author.name,
        author_id=author.author_id,
        birth_date=author.birth_date,
        date_of_death=author.date_of_death,
        biography=author.biography,
        books=books_from_writer[0] if len(books_from_writer) > 0 else None
    )


def add_book(author_id=None):
    author = None
    if author_id is not None:
        author = Author.query.get(author_id)
    if request.method == 'POST':
        title = request.form.get('title', "")
        author_id = request.form.get('author_id', "")
        isbn = request.form.get('isbn', "")
        publication_year = request.form.get('publication_year', "")
        rating = request.form.get('rating', "")
        summary = request.form.get('summary', "")
        book = data_models.add_book(title, author_id, isbn, publication_year, rating, summary)
        author = Author.query.get(author_id)
        return redirect(url_for('show_book', book_id=book.book_id))

    return render_template('add_book.html',
                           author_id = author_id if author_id is not None else "",
                           author_name = author.name if author is not None else "")


def add_author():
    if request.method == 'POST':
        name = request.form.get('name', "")
        birth_date = validate_date(request.form.get('birth_date', ""))
        date_of_death = validate_date(request.form.get('date_of_death', ""))
        biography = request.form.get('biography', "")
        author = data_models.add_author(name, birth_date, date_of_death, biography)
        return redirect(url_for('show_author', author_id=author.author_id))

    return render_template('add_author.html',
                           library_server=LIBRARY_SERVER)

def list_books():
    return render_template('index.html')

def list_authors():
    authors=Author.query.all()
    return render_template('show_authors.html', authors=authors)

def search_author():
    """
    We use this author search query as part of the Add Book form.
    :param search_string:
    :return:
    """
    query = request.args.get('query', '')
    authors = Author.query.filter(Author.name.ilike(f'%{query}%')).all()

    author_data = []
    for author in authors:
        author_data.append({
            'author_id': author.author_id,
            'name': author.name,
            'birth_date': author.birth_date,
            'date_of_death': author.date_of_death,
            'biography': author.biography,
        })

    return jsonify(author_data)


def search_book():
    """
    This function would allow javascript to search for books.
    :return: json response
    """
    query = request.args.get('query', '')
    books = Book.query.filter(Book.title.ilike(f'%{query}%')).all()

    book_data = []
    for book in books:
        book_data.append({
            'author_id': book.author_id,
            'book_id': book.book_id,
            'title': book.title,
            'isbn': book.isbn,
            'publication_year': book.publication_year,
            'rating': book.rating,
            'summary': book.summary,
        })

    return jsonify(book_data)


def search():
    authors = search_author().get_json()
    books = search_book().get_json()
    author_ids = [author.get('author_id', 0) for author in authors]
    book_ids = [book.get('book_id', 0) for book in books]
    query = request.args.get('query', None)
    if query is None or query == '':
        print("Going home")
        return redirect(url_for('home'))
    results = (
        db.session.query(Author, Book)
        .join(Book, Author.author_id == Book.author_id)
        .filter(or_(Author.author_id.in_(author_ids), Book.book_id.in_(book_ids)))
        .order_by(Book.title)
        .all()
    )
    return render_template(
        'home.html',
        results=results,
        query_string=query
    )

def page_not_found(_):
    return render_template('404.html'), 404

def method_not_allowed(_):
    return render_template('405.html'), 405

def internal_error(_):
    return render_template('500.html'), 500
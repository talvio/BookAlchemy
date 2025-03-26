from flask import jsonify, redirect, render_template, request, url_for
import data_models
from datetime import datetime
from data_models import Book, Author

LIBRARY_SERVER = "http://127.0.0.1:5002/"

def validate_date(date_string):
    """ Validate that a date in a string format is a valid date in the format yyyy-mm-dd """
    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d").date()
        return date_obj
    except ValueError:
        return None

def home():
    return render_template('home.html')

def show_book(book_id=None, book=None, author=None):
    if book is None:
        if book_id is None:
            return "I need more information to find the book"
        book = Book.query.filter_by(book_id=book_id).first()
    if author is None:
        author = Author.query.filter_by(author_id=book.author_id).first()
    try:
        raiting = int(book.rating)
    except ValueError:
        raiting = 0
    return render_template('show_book.html',
           title=book.title,
           publication_year=book.publication_year,
           isbn=book.isbn,
           rating=raiting,
           summary=book.summary,
           author=author
    )

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
        authod_id=author.author_id,
        birth_date=author.birth_date,
        date_of_death=author.date_of_death,
        biography=author.biography,
        author_image="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/F_Scott_Fitzgerald_1921.jpg/250px-F_Scott_Fitzgerald_1921.jpg",
        books= books_from_writer
    )


def add_book():
    if request.method == 'POST':
        title = request.form.get('title', "")
        author_id = request.form.get('author_id', "")
        isbn = request.form.get('isbn', "")
        publication_year = request.form.get('publication_year', "")
        rating = request.form.get('rating', "")
        summary = request.form.get('summary', "")
        book = data_models.add_book(title, author_id, isbn, publication_year, rating, summary)
        author = Author.query.get(author_id)
        return show_book(book=book, author=author)

    return render_template('add_book.html')


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

def search_book_author():
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
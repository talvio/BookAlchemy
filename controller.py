import json
from flask import abort, jsonify, redirect, render_template, request, send_from_directory, url_for
from sqlalchemy import desc, or_
from datetime import datetime
import data_models
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
    """ Apparently some browsers need this specific route to ask for the favicon """
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


def home():
    """
    Show the Library Lobby aka home screen.
    home calls the search function to deliver the full experience.
    :return: home page as returned by the search function
    """
    sort_direction = request.args.get('sort_direction', "asc")
    if sort_direction not in ("asc", "desc"):
        sort_direction = "asc"
    sort_by = request.args.get('sort_by', "title")
    if sort_by not in("title", "author", "publication_year"):
        sort_by = "title"
    new_sort_by = request.args.get('new_sort_by')
    if new_sort_by is not None and new_sort_by == sort_by:
        sort_direction = "desc" if sort_direction == "asc" else "asc"
    sort_by = new_sort_by if new_sort_by in ("title", "author", "publication_year") else sort_by
    query = request.args.get('query', "")
    return search(query=query, sort_by=sort_by, sort_direction=sort_direction)


def show_book(book_id=None, book=None, author=None):
    """ Show the chosen book """
    if book is None:
        if book_id is None:
            abort(400)
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


def delete_book(book_id=None,confirmed=None):
    """ Delete the book. """
    if book_id is None:
        request.form.get('book_id', 0)
    book = Book.query.filter_by(book_id=book_id).first()
    if book is None:
        abort(404)
    author = Author.query.filter_by(author_id=book.author_id).first()
    if author is None:
        abort(500)
    if confirmed == False:
        return render_template('relieved.html')
    if confirmed is None:
        return render_template('confirmation.html',
                        question="Do you really want to remove this book?",
                        hidden_json=json.dumps({"book_id": book_id}),
                        yes="Yes, there can be too many books!",
                        no="No, I want to keep it forever!",
                        next_action="delete_book"
        )
    if confirmed == True:
        data_models.delete_book(book)
        return render_template('deleted_book.html', book=book, author=author)
    abort(500)


def confirmation():
    """ Confirm an action and call the action as given by the user. """
    next_action = request.form.get('next_action', None)
    hidden_json = request.form.get('hidden_json', None)
    answer = request.form.get('confirmation', None)
    json_data = json.loads(hidden_json)
    if isinstance(json_data, str):  # Check if it is still a string
        json_data = json.loads(json_data)
    if next_action == "delete_book":
        book_id = json_data.get('book_id', None)
        if answer == 'yes':
            return delete_book(book_id, confirmed=True)
        return render_template('relieved.html')
    abort(500)


def update_book(book_id=None):
    """ Update the book in the database. """
    if book_id is None:
        book_id = request.form.get('book_id', 0)
    book = Book.query.get(book_id)
    author_id = request.form.get('author_id', book.author_id)
    author = Author.query.get(author_id)
    if author is None or book is None:
        abort(404)
    if request.method in ('POST','PUT'):
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
    """ Show the author in the database. """
    if author is None:
        if author_id is None:
            abort(404)
        else:
            author = Author.query.get(author_id)
    books_from_writer = data_models.Book.query.filter(data_models.Book.author_id == author_id).all()
    print(books_from_writer)

    return render_template('show_author.html',
        name=author.name,
        author_id=author.author_id,
        birth_date=author.birth_date,
        date_of_death=author.date_of_death,
        biography=author.biography,
        books=books_from_writer if len(books_from_writer) > 0 else None
    )


def edit_author(author_id):
    """ Edit the author in the database. """
    author = Author.query.get(author_id)
    if author is None:
        abort(404)
    return render_template('edit_author.html', author=author)


def update_author(author_id):
    """ Update the author in the database. """
    author = Author.query.get(author_id)
    if author is None:
        abort(404)
    if request.method in ('POST', 'PUT'):
        author.name = request.form.get('name', author.name)
        author.birth_date = validate_date(request.form.get(
            'birth_date', author.birth_date)
        )
        author.date_of_death = validate_date(request.form.get(
            'date_of_death', author.date_of_death)
        )
        author.biography = request.form.get('biography', author.biography)
        data_models.update_database()
        return redirect(url_for('show_author', author_id=author.author_id))
    abort(405)


def add_book(author_id=None):
    """ Add a new book to the database. """
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
        if Author.query.get(author_id) is None:
            abort(404)
        return redirect(url_for('show_book', book_id=book.book_id))

    return render_template('add_book.html',
                           author_id = author_id if author_id is not None else "",
                           author_name = author.name if author is not None else "")


def add_author():
    """ Add a new author to the database. """
    if request.method == 'POST':
        name = request.form.get('name', "")
        birth_date = validate_date(request.form.get('birth_date', ""))
        date_of_death = validate_date(request.form.get('date_of_death', ""))
        biography = request.form.get('biography', "")
        author = data_models.add_author(name, birth_date, date_of_death, biography)
        return redirect(url_for('show_author', author_id=author.author_id))

    return render_template('add_author.html',
                           library_server=LIBRARY_SERVER)


def list_authors():
    """
    List all authors in the database. This page could use work.
    It does not paginate or sort authors.
    """
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


def search(query=None, sort_by='title', sort_direction='asc'):
    """ Search books and authors matching the query.  """
    order_by = {
        'title': {
            'asc': Book.title,
            'desc': desc(Book.title)
        },
        'author': {
            'asc': Author.name,
            'desc': desc(Author.name)
        },
        'publication_year': {
            'asc': Book.publication_year,
            'desc': desc(Book.publication_year)
        }
    }
    authors = search_author().get_json()
    books = search_book().get_json()
    author_ids = [author.get('author_id', 0) for author in authors]
    book_ids = [book.get('book_id', 0) for book in books]
    if query is None:
        query = request.args.get('query', None)
    results = (
        db.session.query(Author, Book)
        .join(Book, Author.author_id == Book.author_id)
        .filter(or_(Author.author_id.in_(author_ids), Book.book_id.in_(book_ids)))
        .order_by(order_by.get(sort_by, Book.title).get(sort_direction, 'asc'))
        .all()
    )
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    page_scroll = request.args.get('page_scroll')
    if page_scroll == "up":
        page -= 1
    if page_scroll == "down":
        page += 1
    page = max(page, 1)
    start_index = (page - 1) * limit
    if start_index >= len(results):
        start_index = 0
        page = 1
    end_index = start_index + limit
    paginated_result = results[start_index:end_index]
    total_books = len(results)
    total_pages = total_books // limit
    total_pages += 1 if total_books % limit != 0 else 0
    return render_template(
        'home.html',
        results=paginated_result,
        query_string=query,
        sort_by=sort_by,
        sort_direction=sort_direction,
        page=page,
        total_pages=total_pages,
        book_count=total_books
    )


def bad_request(_):
    """ 400 """
    return render_template('400.html'), 400


def page_not_found(_):
    """ 404 """
    return render_template('404.html'), 404


def method_not_allowed(_):
    """ 405 """
    return render_template('405.html'), 405

def internal_error(_):
    """ 500 """
    return render_template('500.html'), 500

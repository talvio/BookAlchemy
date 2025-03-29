from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'

    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    birth_date = db.Column(db.Date)
    date_of_death = db.Column(db.Date)
    biography = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return (f"Author(id = {self.author_id}, "
                f"name = {self.name}, "
                f"birth_date = {self.birth_date}, "
                f"date_of_death = {self.date_of_death})"
        )

    def __str__(self):
        return_str = (f"dbid: ({self.author_id}) "
                      f"{self.name} "
                      f"{self.birth_date} - "
        )
        return_str += f"{self.date_of_death})" if self.date_of_death is not None else ""
        return return_str


class Book(db.Model):
    """ Definition of the book in the SQL database."""
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'), nullable=False)
    isbn = db.Column(db.String(20))
    title = db.Column(db.String(255), nullable=False)
    publication_year = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    summary = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return (f"Book(book_id = {self.book_id}, "
                f"author_id = {self.author_id})"
                f"isbn = {self.isbn}, "
                f"title = {self.title}, "
                f"publication_year = {self.publication_year}, "
                f"rating = {self.rating}, "
                f"summary = {len(self.summary)} characters in db"
        )

    def __str__(self):
        return (f"dbid: ({self.book_id}) "
                f"{self.title} "
                f"({self.publication_year}) "
                f"ISBN: {self.isbn} "
                f"{self.rating}/10"
        )


def add_author(name, birth_date, date_of_death, biography):
    """ Add author to the database.  """
    author = Author()
    author.name = name
    author.birth_date = birth_date
    author.date_of_death = date_of_death
    author.biography = biography
    db.session.add(author)
    db.session.commit()
    return author


def add_book(title, author_id, isbn, publication_year, rating, summary):
    """ Add a book to the database.  """
    book = Book()
    book.title = title
    book.author_id = author_id
    book.isbn = isbn
    book.publication_year = publication_year
    book.rating = rating
    book.summary = summary
    db.session.add(book)
    db.session.commit()
    return book


def delete_book(book):
    """ Delete a book from the database. """
    db.session.delete(book)
    db.session.commit()


def update_database():
    """ Commit changes to the database. """
    db.session.commit()


def get_books_and_ratings(session):
    """ """
    all_books = (
        session.query(Author, Book)
        .join(Book, Author.author_id == Book.author_id)
        #.order_by(order_by.get(sort_by, Book.title).get(sort_direction, 'asc'))
        .all()
    )
    for author, book in all_books:
        if book.rating:
            print(author.name, book.title, book.isbn, book.publication_year, book.rating)


if __name__ == '__main__':
    # Create a database session
    engine = create_engine('sqlite:///data/library.sqlite')
    Session = sessionmaker(bind=engine)
    session = Session()
    get_books_and_ratings(session=session)
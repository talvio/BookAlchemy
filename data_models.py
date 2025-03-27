from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
"""
SQLAlchemy.Model declarative model base class. It sets the table name automatically instead of needing __tablename__.
SQLAlchemy.session is a session that is scoped to the current Flask application context. It is cleaned up after every request.
SQLAlchemy.metadata and SQLAlchemy.metadatas gives access to each metadata defined in the config.
SQLAlchemy.engine and SQLAlchemy.engines gives access to each engine defined in the config.
SQLAlchemy.create_all() creates all tables.
You must be in an active Flask application context to execute queries and to access the session and engine.
"""

# Create a database session
#Session = sessionmaker(bind=engine)
#session = Session()

# Define the data table class's parent class
#Base = declarative_base()


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
        return_str = (f"dbid: ({self.id}) "
                      f"{self.name} "
                      f"{self.birth_date} - "
        )
        return_str += f"{self.date_of_death})" if self.date_of_death is not None else ""
        return return_str


class Book(db.Model):
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
    author = Author()
    author.name = name
    author.birth_date = birth_date
    author.date_of_death = date_of_death
    author.biography = biography
    db.session.add(author)
    db.session.commit()
    return author

def add_book(title, author_id, isbn, publication_year, rating, summary):
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

def get_all_books():
    pass

def update_author(author):
    pass

def update_book(book):
    pass




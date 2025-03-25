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
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'))
    isbn = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    publication_year = db.Column(db.Integer)

    def __repr__(self):
        return (f"Book(book_id = {self.book_id}, "
                f"author_id = {self.author_id})"
                f"isbn = {self.isbn}, "
                f"title = {self.title}, "
                f"publication_year = {self.publication_year}"
        )

    def __str__(self):
        return (f"dbid: ({self.book_id}) "
                f"{self.title} "
                f"({self.publication_year}) "
                f"ISBN: {self.book_isbn}"
        )




from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import app_routes
from data_models import db, Author, Book
from sqlalchemy import inspect
from pathlib import Path
import app_routes

SQL_URI = "sqlite:///" + str(Path(__file__).parent / "data/library.sqlite")

def setup_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = SQL_URI # 'sqlite:///data/library.sqlite'
    db.init_app(flask_app)
    with flask_app.app_context():
        inspector = inspect(db.engine)
        if ('authors' not in inspector.get_table_names()
            or 'books' not in inspector.get_table_names()):
            db.create_all()
    return flask_app

if __name__ == '__main__':
    print(SQL_URI)
    app = setup_app()
    app_routes.define_flask_routes(app)
    app.run(host="0.0.0.0", port=5002, debug=True)

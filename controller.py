from flask import render_template, url_for

def add_book():
    return "Add Book"

def list_books():
    return render_template('index.html')
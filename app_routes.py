import controller


def define_flask_routes(app):

    @app.route('/favicon.ico')
    def favicon():
        return controller.send_favicon()

    @app.route('/', methods=['GET'])
    def home():
        """ The Library home page, list of books and authors."""
        return controller.home()

    @app.route('/add_book', methods=['POST', 'GET'])
    def add_book():
        """ Add new book to the library."""
        return controller.add_book()

    @app.route('/add_author_book/<int:author_id>', methods=['POST', 'GET'])
    def add_author_book(author_id):
        """ Add new book with the author_id given"""
        return controller.add_book(author_id=author_id)

    @app.route('/add_author', methods=['POST', 'GET'])
    def add_author():
        """ Add new author to the library."""
        return controller.add_author()

    @app.route('/show_author/<int:author_id>', methods=['GET'])
    def show_author(author_id):
        """ Show details of a the author"""
        return controller.show_author(author_id=author_id)


    @app.route('/list_authors', methods=['GET'])
    def list_authors():
        """ List all authors in the library. """
        return controller.list_authors()

    @app.route('/search', methods=['GET'])
    def search():
        """ Search for books and authors in the library. """
        return controller.search()

    @app.route('/show_book/<int:book_id>', methods=['GET'])
    def show_book(book_id):
        """ Show details of a book in the library. """
        return controller.show_book(book_id=book_id)

    @app.route('/edit_book/<int:book_id>', methods=['GET'])
    def edit_book(book_id):
        """ Edit the book. """
        return controller.edit_book(book_id=book_id)

    @app.route('/update_book/<int:book_id>', methods=['PUT', 'POST'])
    def update_book(book_id):
        """ Update a book in the library."""
        return controller.update_book(book_id)

    @app.route('/search_author', methods=['GET'])
    def search_author():
        """ Search for the author using a query string. """
        return controller.search_author()


    @app.route('/search_book', methods=['GET'])
    def search_book():
        pass
        #return controller.search_book()

    @app.errorhandler(404)
    def page_not_found(_):
        """ Page not found error"""
        return controller.page_not_found(_)

    @app.errorhandler(405)
    def method_not_allowed(_):
        """ Page not found error"""
        return controller.method_not_allowed(_)

    @app.errorhandler(500)
    def internal_error(_):
        """ Oh, oh! Something went wrong and we saw it happen. """
        return controller.internal_error(_)
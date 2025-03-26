import controller

def define_flask_routes(app):
    @app.route('/', methods=['GET'])
    def home():
        return controller.home()

    @app.route('/add_book', methods=['POST', 'GET'])
    def add_book():
        return controller.add_book()

    @app.route('/add_author', methods=['POST', 'GET'])
    def add_author():
        return controller.add_author()

    @app.route('/show_author/<int:author_id>', methods=['GET'])
    def show_author(author_id):
        return controller.show_author(author_id=author_id)

    @app.route('/list_books', methods=['GET'])
    def list_books():
        return controller.list_books()


    @app.route('/list_authors', methods=['GET'])
    def list_authors():
        return controller.list_authors()

    @app.route('/search', methods=['GET'])
    def search():
        pass

    @app.route('/search_book', methods=['GET'])
    def search_book():
        pass

    @app.route('/search_book_author', methods=['GET'])
    def search_book_author():
        return controller.search_book_author()

    @app.route('/search_author', methods=['GET'])
    def search_author():
        pass
        #return controller.search_book_author()

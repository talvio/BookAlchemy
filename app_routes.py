import controller

def define_flask_routes(app):
    @app.route('/add_book', methods=['POST'])
    def add_book():
        return controller.add_book()

    @app.route('/add_book', methods=['GET'])
    def list_books():
        return controller.list_books()
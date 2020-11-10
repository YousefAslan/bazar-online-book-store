from flask.globals import request
from server_configuration import *

@catalog_server.route("/search/<string:topic>",methods=['GET'])
def search(topic):
    books = Book.query.filter_by(topic= topic).all()
    return books_search_schema.jsonify(books)

@catalog_server.route("/lookup/<int:id>",methods=['GET'])
def lookup(id):
    books = Book.query.filter_by(id = id).first()
    return book_lookup_schema.jsonify(books)

@catalog_server.route("/verify_item_in_stock/<int:id>",methods=['GET'])
def verify_item_in_stock(id):
    book = Book.query.filter_by(id = id).first()
    return verify_schema.jsonify(book)

@catalog_server.route("/update/<int:id>",methods=['PUT'])
def update(id):
    book = Book.query.get(id)
    try:
        if book.quantity > 0:
            book.quantity -= 1
            db.session.commit()
            return {}, 204
        else:
            return {"message": "Gone", "description": "This book is currently unavailable"}, 410
    except:
        return {"message": "Not Found", "description": "There is no book with this ID"}, 404
    

@catalog_server.route("/append",methods=['POST'])    
def append():
    print(request)
    title = request.json['title']
    quantity = request.json['quantity']
    cost = request.json['cost']
    topic = request.json['topic']

    new_book = Book(title,quantity,cost,topic)
    db.session.add(new_book)
    db.session.commit()
    return book_search_schema.jsonify(new_book)

@catalog_server.errorhandler(404)
def resource_could_not_found(e):
    return jsonify({'error': 404}), 404

@catalog_server.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 405}), 405

if __name__ == "__main__":
    catalog_server.run(debug = True, port = 2310)
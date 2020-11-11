from flask.globals import request
from server_configuration import *

@catalog_server.route("/search/<string:topic>",methods=['GET'])
def search(topic):
    books = Book.query.filter_by(topic= topic).all()
    if len(books) > 0:
        return books_search_schema.jsonify(books)
    else:
        return {"message": "There are no books under this topic"}, 410
    
@catalog_server.route("/lookup/<int:id>",methods=['GET'])
def lookup(id):
    book = Book.query.get(id)
    if book:
        return book_lookup_schema.jsonify(book), 200
    else:
        return {"message" : "There is no book with this ID"}, 404
    
@catalog_server.route("/verify_item_in_stock/<int:id>",methods=['GET'])
def verify_item_in_stock(id):
    book = Book.query.get(id)
    if book:
        if book.quantity > 0:
            return verify_schema.jsonify(book), 200
        else:
            return {"message": "This book is currently unavailable"}, 410
    else:
        return {"message": "There is no book with this ID"}, 404

@catalog_server.route("/update/<int:id>",methods=['PUT'])
def update(id):
    book = Book.query.get(id)
    if book:
        if book.quantity > 0:
            book.quantity -= 1
            db.session.commit()
            return {}, 204
        else:
            return {"message": "This book is currently unavailable"}, 410
    else:
        return {"message": "There is no book with this ID"}, 404
    

@catalog_server.route("/append",methods=['POST'])    
def append():
    try:
        title = request.json['title']
        quantity = request.json['quantity']
        cost = request.json['cost']
        topic = request.json['topic']

        new_book = Book(title,quantity,cost,topic)
        db.session.add(new_book)
        db.session.commit()
        return book_lookup_schema.jsonify(new_book), 201
    except:
        return {"message" : "cant add this book"}, 405
    

@catalog_server.errorhandler(404)
def resource_could_not_found(e):
    return jsonify({'error': 404}), 404

@catalog_server.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 405}), 405

if __name__ == "__main__":
    catalog_server.run(debug = True, port = 2310)
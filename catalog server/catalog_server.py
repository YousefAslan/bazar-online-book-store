from flask.globals import request
import requests
import numbers
from server_configuration import *


@catalog_server.route("/search/<string:topic>", methods=['GET'])
def search(topic):
    """
    handle the comming request form the front-end server to get all book with topic shown inside the get request
    """
    try:
        # try to get orders from database under this topic
        books = Book.query.filter_by(topic=topic).all()
        if len(books) > 0:
            # if there is books under this topic return list contains them
            return books_schema.jsonify(books), 200
        else:
            return {"message": "There are no books under this topic"}, 404
    except:
        return {"message": "There are no books under this topic"}, 404


@catalog_server.route("/lookup/<int:id>", methods=['GET'])
def lookup(id):
    """
    handle the comming request form the front-end server to get more infromation about specific booksing its id shown inside the get request
    """
    # get the book with id sends inside the request
    book = Book.query.get(id)
    # check if there is a book with that id if not send a message with 404 says there is no book with this id
    if book:
        # return a responce with the book infromation from title, quantity, and cost
        return book_schema.jsonify(book), 200
    else:
        return {"message": "There is no book with this ID"}, 404


@catalog_server.route("/verify_item_in_stock/<int:id>", methods=['GET'])
def verify_item_in_stock(id):
    """
    this request came from order server to check the quantity of the item specified via ID
    """
    # get the book with id
    book = Book.query.get(id)
    # check if there is a book with that id if not send a message with 404 says there is no book with this id
    if book:
        # if book found check if its exist at the stock if send responce with 200 status code and its id and the quantity
        # if nits out of stock send message says This book is currently unavailable
        if book.quantity > 0:
            return verify_schema.jsonify(book), 200
        else:
            return {"message": "This book is currently unavailable"}, 410
    else:
        return {"message": "There is no book with this ID"}, 404


@catalog_server.route("/update/price/<int:id>", methods=['PUT'])
def update_cost(id):
    """
    update the price for the book with id send to this end-point
    the body request contains the new price
    """
    # get the book from database
    book = Book.query.get(id)
    # prepare the response
    headers = {'Content-type': 'application/json'}
    json = None
    if book:
        # check the correctness of the body request
        if 'price' in request.json and isinstance(request.json['price'], numbers.Number):
            # update the book price
            book.cost = request.json['price']
            try:
                # send invalidate to the frint-end server to delete this instance from the cache
                response = requests.delete(
                    front_end_server + '/invalidate/' + str(id), timeout=(0.3, 2))
            except:
                pass
            headers = {'Content-type': 'application/json'}
            json = book_schema.dump(book)
            try:
                # try to send sync to the 2nd catalog server
                response = requests.put(
                    second_catalog_server + '/sync', headers=headers, json=json)
            except:
                # if the catalog does not respond send it to recovery server
                json["server"] = second_catalog_server
            try:
                response = requests.post(
                    recovery_server + '/addBook', json=json, headers=headers)
            except:
                return {"message": "The server is not ready to handle the request"}, 503
            # commit the unpdate
            db.session.commit()
            return book_schema.jsonify(book), 200

        else:
            return {"message": "bad request can not handle the request due to invaled data"}, 400
    else:
        return {"message": "There is no book with this ID"}, 404


@catalog_server.route("/update/item/<int:id>", methods=['PUT'])
def update_item_number(id):
    """
    update the quantity for the book with id send to this end-point
    the body request contains the new quantity
    """
    # get the book from database
    book = Book.query.get(id)
    if book:
        # check the correctness of the body request
        if 'quantity' in request.json and isinstance(request.json['quantity'], numbers.Number):
            book.quantity = request.json['quantity']
            try:
                # send invalidate to the front-end server to delete this instance from the cache
                response = requests.delete(
                    front_end_server + '/invalidate/' + str(id), timeout=(0.3, 2))
            except:
                pass
            headers = {'Content-type': 'application/json'}
            json = book_schema.dump(book)
            try:
                # try to send sync to the 2nd catalog server
                response = requests.put(
                    second_catalog_server + '/sync', headers=headers, json=json)
            except:
                # if the catalog does not respond send it to recovery server
                json["server"] = second_catalog_server
            try:
                response = requests.post(
                    recovery_server + '/addBook', json=json, headers=headers)
            except:
                return {"message": "The server is not ready to handle the request"}, 503
            # commit the unpdate
            db.session.commit()
            return book_schema.jsonify(book), 200
        else:
            return {"message": "bad request can not handle the request due to invaled data"}, 400
    else:
        return {"message": "There is no book with this ID"}, 404


@catalog_server.route("/buy/<int:id>", methods=['PUT'])
def buy(id):
    """
    apply the buy methos comes from the oder server

    """
    # get the book with id sends inside the request
    book = Book.query.get(id)
    if book:
        # if the book exsist in side the stocks decremnt it and update the changes
        # and return 204 status code indicates that the request has succeeded
        if book.quantity > 0:
            book.quantity -= 1
            try:
                # try to push invalidate notification to the front end server
                response = requests.delete(
                    front_end_server + '/invalidate/' + str(id), timeout=(0.3, 2))
            except:
                pass
            headers = {'Content-type': 'application/json'}
            json = book_schema.dump(book)
            try:
                # try to push update notification to the second catalog server
                response = requests.put(
                    second_catalog_server + '/sync', headers=headers, json=json, timeout=(0.3, 2))
            except:
                json["server"] = second_catalog_server
            try:
                response = requests.post(
                    recovery_server + '/addBook', json=json, headers=headers, timeout=(0.3, 5))
            except:
                return {"message": "The server is not ready to handle the request"}, 503
            db.session.commit()
            return {}, 204
        else:
            # otherwise if out of stock return a message says This book is currently unavailable
            return {"message": "This book is currently unavailable"}, 410
    else:
        return {"message": "There is no book with this ID"}, 404


@catalog_server.route("/sync", methods=['PUT'])
def syncUpDateInfo():
    """
    handle the sync between catalog servers
    if other cataolg servers update there database 
    the sync update info will be called to infrom this server about this updates
    """
    book = None
    try:
        book = Book.query.get(request.json['id'])
        if book:
            book.title = request.json['title']
            book.quantity = request.json['quantity']
            book.cost = request.json['cost']
            book.topic = request.json['topic']
        else:
            new_book = Book(request.json['title'], request.json['quantity'],
                            request.json['cost'], request.json['topic'])
            db.session.add(new_book)
    except:
        return {"message": " the server cannot or will not process the request due to something perceived to be a client error"}, 400

    db.session.commit()
    return book_schema.jsonify(book), 200


@catalog_server.route("/append", methods=['POST'])
def append():
    """
    append new books into the database
    """
    try:
        title = request.json['title']
        quantity = request.json['quantity']
        cost = request.json['cost']
        topic = request.json['topic']

        new_book = Book(title, quantity, cost, topic)
        db.session.add(new_book)
        db.session.commit()
        return book_lookup_schema.jsonify(new_book), 201
    except:
        return {"message": "cant add this book"}, 405


@catalog_server.before_first_request
def checkAnyUpdates():
    """
    before first request the server check if there is any updates inside the recovery server
    """
    try:
        headers = {'Content-type': 'application/json'}
        json = {'server': this_server}
        # send getUpdates to recovery server
        response = requests.get(
            recovery_server + '/getUpdates', headers=headers, json=json, timeout=(0.3, 5))
        book = None
        # for each update check if there is book with same id
        # if there is update it else create a new one
        for updatedBook in response.json():
            book = Book.query.get(updatedBook['id'])
            if book:
                book.title = updatedBook['title']
                book.quantity = updatedBook['quantity']
                book.cost = updatedBook['cost']
                book.topic = updatedBook['topic']
            else:
                pass
                # book = Book(id= updatedBook['id'],cost= updatedBook['cost'], quantity= updatedBook['quantity'], title= updatedBook['title'], topic= updatedBook['topic'])
                # db.session.add(book)
            db.session.commit()
    except:
        pass


@catalog_server.errorhandler(404)
def resource_could_not_found(e):
    return jsonify({'error': 404}), 404


@catalog_server.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 405}), 405


if __name__ == "__main__":
    catalog_server.run(debug=True, port=2030, host='0.0.0.0')

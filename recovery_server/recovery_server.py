from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
import os


#initi order server
recovery_server = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#initi database
recovery_server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'recovery.sqlite')
recovery_server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(recovery_server)
ma = Marshmallow(recovery_server)


class Orders(db.Model):
    server = db.Column(db.String(200), primary_key=True)
    order_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer)

    def __init__(self, server, order_id, book_id):
        self.server = server
        self.order_id = order_id
        self.book_id = book_id
        
class OrderSchema(ma.Schema):
  class Meta:
    fields = ('server', 'order_id', 'book_id')

class Book(db.Model):
    """

    """
    id = db.Column(db.Integer, primary_key=True)
    server = db.Column(db.String(200), primary_key=True)
    title = db.Column(db.String(200))
    quantity = db.Column(db.Integer)
    cost = db.Column(db.Float)
    topic = db.Column(db.String(200))

    def __init__(self, id, server, title, quantity, cost, topic):
        self.id = id
        self.server = server
        self.title = title
        self.quantity = quantity
        self.cost = cost
        self.topic = topic    

class BookSchema(ma.Schema):
  class Meta:
    fields = ('id', 'server', 'title', 'quantity', 'cost', 'topic')

order_schema = OrderSchema()
book_schema = BookSchema()
orders_schema = OrderSchema(many=True)
books_schema = BookSchema(many = True)


@recovery_server.route("/addBook",methods=['POST'])
def addBook():
    try:
        id = request.json['id']
        server = request.json['server']
        title = request.json['title']
        quantity = request.json['quantity']
        cost = request.json['cost']
        topic = request.json['topic']

        new_book = Book(id, server, title, quantity, cost, topic)
        try:
            book = Book.query.filter_by(server= server, id =id).first()
            book.title = title
            book.quantity = quantity
            book.cost = cost
            book.topic = topic
            db.session.commit()
        except:
            db.session.add(new_book)
            db.session.commit()
        return book_schema.jsonify(new_book), 201
    except:
        return {"message" : "cant add this book"}, 405

@recovery_server.route("/addOrder",methods=['POST'])
def addOrder():
    try:
        server = request.json['server']
        order_id = request.json['order_id']
        book_id = request.json['book_id']

        new_order = Orders(server, order_id, book_id)
        try:        
            order = Orders.query.filter_by(server= server, id =id).first()
            order.server = server
            order.order_id = order_id
            order.book_id = book_id
            db.session.commit()
        except:
            db.session.add(new_order)
            db.session.commit()
        
        return order_schema.jsonify(new_order), 201
    except:
        return {"message" : "cant add this order"}, 405   

@recovery_server.route("/getOrder/<string:server>",methods=['GET'])
def getOrder(server):
    orders = Orders.query.filter_by(server= server)
    toReturn = orders_schema.jsonify(orders.all())
    orders.delete()
    db.session.commit()
    return toReturn, 200

@recovery_server.route("/getUpdates/<string:server>",methods=['GET'])
def getUpdates(server):
    book = Book.query.filter_by(server= server)
    toReturn = books_schema.jsonify(book.all())
    book.delete()
    db.session.commit()
    return toReturn, 200

@recovery_server.errorhandler(404)
def resource_could_not_found(e):
    return jsonify({'error': 404}), 404

@recovery_server.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 405}), 405

if __name__ == "__main__":
    recovery_server.run(debug = True, port = 2050, host= '0.0.0.0')
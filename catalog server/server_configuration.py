from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
import os

# font_end_server_ip = "192.168.199.4"
# font_end_server_port = 2309
# order_server_ip = "192.168.199.3"
# order_server_port = 2311
# catalog_server_ip = "192.168.199.5"
# catalog_server_port = 2310
# font_end_server_ip = "172.0.0.1"
# font_end_server_port = 2309
# order_server_ip = "172.0.0.1"
# order_server_port = 2309

# init flask calalog server which responce to handle the requests comming from the front-end and order-servers
catalog_server = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
"""
init the database which allocated at the catalog server directory 
use SQL Alchemy and Marshmallow to interact with the database via object relational mapper,
which makes it easy to interact with databse, apply updates on it, and simplify the queries
"""
catalog_server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'catalog_database.sqlite')
catalog_server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(catalog_server)
ma = Marshmallow(catalog_server)

class Book(db.Model):
  """
  Book class Inherit db.model
  It is a class present in SQLAlchemy and aims to facilitate dealing with the database and works on representing entities in it
  book contains four basic information in it that are stored in the database table and they are: name, title, cost, and quantity.
  The title column represents the name(title) of the book
  while topic of books belong to one of two topics distributed systems and graduate school
  the quantity column maintains the number of items in stock from each book
  and the cost of the book

  """
  id = db.Column(db.Integer, primary_key=True, unique=True)
  title = db.Column(db.String(200))
  quantity = db.Column(db.Integer)
  cost = db.Column(db.Float)
  topic = db.Column(db.String(200))

  def __init__(self, title, quantity, cost, topic):
    self.title = title
    self.quantity = quantity
    self.cost = cost
    self.topic = topic      

"""
  Book search Schema Schema, Book lookup Schema, and Verify Schema all are flask marshmallow schema
  which makes it easy to convert database queries results into data that can be read and sent in the responce
"""
class BookSearchSchema(ma.Schema):
  class Meta:
    fields = ('id', 'title')

class BooklookupSchema(ma.Schema):
  class Meta:
    fields = ('title', 'quantity', 'cost')

class VerifySchema(ma.Schema):
  class Meta:
    fields = ('id', 'quantity')

# create an instance of the diagrams for use on the server
books_search_schema = BookSearchSchema(many=True)
book_lookup_schema = BooklookupSchema()
verify_schema = VerifySchema()

      



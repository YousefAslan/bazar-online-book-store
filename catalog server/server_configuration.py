from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
from enum import Enum
import os


class ServerType(Enum):
    """
    represent the server
    """
    FRONT = 1
    CATALOG = 2
    ORDER = 3
    
class RequestType(Enum):
    """
    represent the server
    """
    SEARCH = 1
    LOOKUP = 2
    UPDATE = 3
    BUY = 4

front_end_server = "http://127.0.0.1:2020"
this_server = "http://127.0.0.1:2030"
second_catalog_server = "http://127.0.0.1:2031"
recovery_server = "http://127.0.0.1:2050"

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
class BookSchema(ma.Schema):
  class Meta:
    fields = ('id', 'title', 'quantity', 'cost', 'topic')

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
book_schema = BookSchema()
books_schema = BookSchema(many = True)

books_search_schema = BookSearchSchema(many=True)
book_lookup_schema = BooklookupSchema()
verify_schema = VerifySchema()

      



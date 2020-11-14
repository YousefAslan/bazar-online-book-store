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

#initi catalog server
catalog_server = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#initi database
catalog_server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'catalog_database.sqlite')
catalog_server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(catalog_server)
ma = Marshmallow(catalog_server)

class Book(db.Model):
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

# Book Schema
class BookSearchSchema(ma.Schema):
  class Meta:
    fields = ('id', 'title')

class BooklookupSchema(ma.Schema):
  class Meta:
    fields = ('title', 'quantity', 'price')

class VerifySchema(ma.Schema):
  class Meta:
    fields = ('id', 'quantity')

# Init schema
books_search_schema = BookSearchSchema(many=True)
book_lookup_schema = BooklookupSchema()
verify_schema = VerifySchema()

      



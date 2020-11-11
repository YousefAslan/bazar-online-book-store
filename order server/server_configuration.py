from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
import os

font_end_server_ip = "http://127.0.0.1"
font_end_server_port = 2309
catalog_server_ip = "http://127.0.0.1"
catalog_server_port = 2310


#initi order server
order_server = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#initi database
order_server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'order_database.sqlite')
order_server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(order_server)
ma = Marshmallow(order_server)

class Orders(db.Model):
  order_id = db.Column(db.Integer, primary_key=True, unique=True)
  book_id = db.Column(db.Integer)

  def __init__(self, book_id):
    self.book_id = book_id

class OrderSchema(ma.Schema):
  class Meta:
    fields = ('order_id', 'book_id')

order_schema = OrderSchema()
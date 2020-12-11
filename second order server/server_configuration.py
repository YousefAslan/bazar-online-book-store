from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
import os

front_end_server = "http://127.0.0.1:2020"
this_server = "http://127.0.0.1:2041"
catalog_server = "http://127.0.0.1:2031"
second_order_server = "http://127.0.0.1:2040"
recovery_server = "http://127.0.0.1:2050"

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
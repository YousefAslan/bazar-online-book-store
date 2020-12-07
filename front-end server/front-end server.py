from flask import Flask, request, jsonify
from flask import json
import requests
from enum import Enum
import os

class ServerType(Enum):
    """
    represent the server
    """
    CATALOG = 1
    LOOKUP = 2


# font_end_server_ip = "192.168.199.4"
# font_end_server_port = 2309
# order_server_ip = "192.168.199.3"
# order_server_port = 2311
# catalog_server_ip = "192.168.199.5"
# catalog_server_port = 2310
order_server_ip = "http://127.0.0.1"
order_server_port = 2311
catalog_server_ip = "http://127.0.0.1"
catalog_server_port = 2310

app = Flask(__name__)

@app.route('/search/<string:topic>',methods = ['GET'])
def search(topic):
    """
    mapping the coming get request on the route search/<topic> to the method search
    The search method aims to send the request coming from the end-user to the catalog server to be processed there
    and await a response from the catalog to be responded on the end-user.

    """
    responce = requests.get(catalog_server_ip + ':' + str(catalog_server_port) + '/search/' + topic)
    return jsonify(responce.json()), responce.status_code

@app.route('/lookup/<int:id>',methods = ['GET'])
def lookup(id):
    """
    mapping the coming get request on the route lookup/<id> to lookup method
    It aims to send the incoming get request to the catalog server to deal with it
    and response to the end-user

    """
    responce = requests.get(catalog_server_ip + ':' + str(catalog_server_port) + '/lookup/' + str(id))
    return jsonify(responce.json()), responce.status_code

@app.route('/buy/<int:id>',methods = ['PUT'])
def buy(id):
    """
    mapping the coming put request on the route buy/<id> to buy method
    Their purpose is to purchase this item based on the attached id and url by sending it to another server called order server
    to handle the purchase process and with response which indicate if this process done or not

    """
    responce = requests.put(order_server_ip + ':' + str(order_server_port) + '/buy/' + str(id))
    return jsonify(responce.json()), responce.status_code

@app.route("/update/price/<int:id>",methods=['PUT'])
def update_price(id):
    """
    mapping the coming put request on the route /update/price/<id> to update_price method
    Their purpose is to send a put request to the catalog server to update the price of a spacefice item based on the id

    """
    headers = {'Content-type': 'application/json'}
    jsons = request.json
    responce = requests.put(catalog_server_ip + ':' + str(catalog_server_port) + '/update/price/' + str(id), json= jsons, headers =headers)
    return jsonify(responce.json()), responce.status_code

@app.route("/update/item/<int:id>",methods=['PUT'])
def update_item_number(id):
    """
    mapping the coming put request on the route /update/item/<id> item_number method
    Their purpose is to send a put request to the catalog server to update number of items avaibale from the product

    """
    headers = {'Content-type': 'application/json'}
    jsons = request.json
    responce = requests.put(catalog_server_ip + ':' + str(catalog_server_port) + '/update/item/' + str(id), json= jsons, headers =headers)
    return jsonify(responce.json()), responce.status_code

@app.errorhandler(404)
def resource_could_not_found(e):
    """
    this method responce if the end user send a request asking from URL that deos not exist such as /update/name/id

    """
    return jsonify({'message': "server can't find the requested resource."}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'message': " the server but is not supported by the target resource"}), 405

if __name__ == '__main__':
  app.run(debug = True, port = 2309, host='0.0.0.0')
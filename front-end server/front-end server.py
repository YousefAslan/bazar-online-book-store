from flask import Flask, request, jsonify
from flask import json
import requests
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

order_server_ip = "http://127.0.0.1"
order_server_port = 2311
catalog_server_ip = "http://127.0.0.1"
catalog_server_port = 2310

catalog_servers = ["http://127.0.0.1:2310",]
order_servers = ["http://127.0.0.1:2311", ]
nextSelectedServer = 0

app = Flask(__name__)

@app.route('/search/<string:topic>',methods = ['GET'])
def search(topic):
    """
    mapping the coming get request on the route search/<topic> to the method search
    The search method aims to send the request coming from the end-user to the catalog server to be processed there
    and await a response from the catalog to be responded on the end-user.

    """
    # TODO: implement the cache
    # cache miss ask the server
    if not checkCache(RequestType.SEARCH ,topic) : 
        for attempt in range(len(catalog_servers)):
            selectedServer = selectServer(ServerType.CATALOG)
            try:
                responce = requests.get(selectedServer + '/search/' + topic)
                # save to the cache
                return jsonify(responce.json()), responce.status_code
            except:
                pass
        return {"message": " server is not ready to handle the request"}, 503
    else:
        # return the cache value 
        return {},500


@app.route('/lookup/<int:id>',methods = ['GET'])
def lookup(id):
    """
    mapping the coming get request on the route lookup/<id> to lookup method
    It aims to send the incoming get request to the catalog server to deal with it
    and response to the end-user

    """
    if not checkCache(RequestType.LOOKUP ,id) : 
        for attempt in range(len(catalog_servers)):
            selectedServer = selectServer(ServerType.CATALOG)
            try:
                responce = requests.get(selectedServer + '/lookup/' + str(id))
                # save to the cache
                return jsonify(responce.json()), responce.status_code
            except:
                pass
        return {"message": " server is not ready to handle the request"}, 503
    else:
        # return the cache value 
        return {},500

@app.route("/update/price/<int:id>",methods=['PUT'])
def update_price(id):
    """
    mapping the coming put request on the route /update/price/<id> to update_price method
    Their purpose is to send a put request to the catalog server to update the price of a spacefice item based on the id

    """
    
    headers = {'Content-type': 'application/json'}
    jsons = request.json
    for attempt in range(len(catalog_servers)):
        selectedServer = selectServer(ServerType.CATALOG)
        try:
            responce = requests.put(selectedServer + '/update/price/' + str(id), json = jsons, headers = headers)
            return jsonify(responce.json()), responce.status_code
        except:
            pass
    return {"message": " server is not ready to handle the request"}, 503

@app.route("/update/item/<int:id>",methods=['PUT'])
def update_item_number(id):
    """
    mapping the coming put request on the route /update/item/<id> item_number method
    Their purpose is to send a put request to the catalog server to update number of items avaibale from the product

    """
    headers = {'Content-type': 'application/json'}
    jsons = request.json
    for attempt in range(len(catalog_servers)):
        selectedServer = selectServer(ServerType.CATALOG)
        try:
            responce = requests.put(selectedServer + '/update/item/' + str(id), json = jsons, headers = headers)
            return jsonify(responce.json()), responce.status_code
        except:
            pass
    return {"message": " server is not ready to handle the request"}, 503


@app.route('/buy/<int:id>',methods = ['PUT'])
def buy(id):
    """
    mapping the coming put request on the route buy/<id> to buy method
    Their purpose is to purchase this item based on the attached id and url by sending it to another server called order server
    to handle the purchase process and with response which indicate if this process done or not

    """

    for attempt in range(len(catalog_servers)):
        selectedServer = selectServer(ServerType.ORDER)
        try:
            responce = requests.put(selectedServer + '/buy/' + str(id))
            return jsonify(responce.json()), responce.status_code
        except:
            pass
    return {"message": " server is not ready to handle the request"}, 503

# TODO: not implemented yet
@app.route('/invalidate/<int:id>', methods = ['DELETE'])
def invalidate(id):
    """
    invalidate request comes from any back-end server to invalidate item cached value
    """
    return {"message": "the item removed from the cache"}, 200

@app.errorhandler(404)
def resource_could_not_found(e):
    """
    this method responce if the end user send a request asking from URL that deos not exist such as /update/name/id

    """
    return jsonify({'message': "server can't find the requested resource."}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'message': " the server but is not supported by the target resource"}), 405

def selectServer(serverType: ServerType):
    """
    select which replica responsible for handling this request
    """

    selectedServer = (++nextSelectedServer) % len(order_servers)
    return catalog_servers[selectedServer] if serverType == ServerType.CATALOG else order_servers[selectedServer]

# TODO: not implemented yet
def checkCache(requestType: RequestType, data):
    """
    docstring
    """
    return False

if __name__ == '__main__':
  app.run(debug = True, port = 2309, host='0.0.0.0')
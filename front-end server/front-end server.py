from flask import Flask, request, jsonify
import requests
import os

order_server_ip = "http://127.0.0.1"
order_server_port = 2311
catalog_server_ip = "http://127.0.0.1"
catalog_server_port = 2310

app = Flask(__name__)


@app.route('/search/<string:topic>',methods = ['GET'])
def search(topic):
    responce = requests.get(catalog_server_ip + ':' + str(catalog_server_port) + '/search/' + topic)
    print(type(responce.json()))
    print(responce.json())
    return jsonify(responce.json()), responce.status_code

@app.route('/lookup/<int:id>',methods = ['GET'])
def lookup(id):
    responce = requests.get(catalog_server_ip + ':' + str(catalog_server_port) + '/lookup/' + str(id))
    return jsonify(responce.json()), responce.status_code

@app.route('/buy/<int:id>',methods = ['PUT'])
def buy(id):
    responce = requests.put(order_server_ip + ':' + str(order_server_port) + '/buy/' + str(id))
    return jsonify(responce.json()), responce.status_code

@app.errorhandler(404)
def resource_could_not_found(e):
    return jsonify({'error': 404}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 405}), 405

if __name__ == '__main__':
  app.run(debug = True, port = 2309)
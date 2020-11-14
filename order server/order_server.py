from requests.api import request
from server_configuration import *
import requests

@order_server.route("/buy/<int:id>",methods=['PUT'])    
def buy(id):
    try:
        responce = requests.get(catalog_server_ip + ':' + str(catalog_server_port) + '/verify_item_in_stock/' + str(id))
        if responce.status_code == 200 and responce.json()['quantity'] > 0:
            responce = requests.put(catalog_server_ip + ':' + str(catalog_server_port) + '/buy/' + str(id))
            if responce.status_code == 204:
                orders = Orders(id)
                db.session.add(orders)
                db.session.commit()
                return order_schema.jsonify(orders), 201
            else:
                return {"message": "This book is currently unavailable"}, 410
        else:
            return {"message": "This book is currently unavailable"}, 410
    except :
        return {"message": "This book is currently unavailable"}, 410

@order_server.errorhandler(404)
def resource_could_not_found(e):
    return jsonify({'error': 404}), 404

@order_server.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'errdor': 405}), 405

if __name__ == "__main__":
    order_server.run(debug = True, port = 2311, host= '0.0.0.0')
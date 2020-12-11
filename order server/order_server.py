from recovery_server.recovery_server import Orders
from flask.globals import request
import requests
from server_configuration import *

@order_server.route("/buy/<int:id>",methods=['PUT'])    
def buy(id):
    """
    this method response to handle the buy request comes from the fron-end server to be completed the purchase order
    """
    try:
        # ensure that the book is in stocks vias send requiest to the catalog server
        responce = requests.get(catalog_server + '/verify_item_in_stock/' + str(id))
        #  if status code 200 and which means there is books at the stock
        # to completed the purchase order send buy request for the catalog server
        if  responce.status_code == 200 and responce.json()['quantity'] > 0:
            responce = requests.put(catalog_server + '/buy/' + str(id))
            if responce.status_code == 204:
                orders = Orders(id)
                db.session.add(orders)
                db.session.commit()
                headers = {'Content-type': 'application/json'}
                json = order_schema.dump(orders)
                try:
                    responce = requests.put(second_order_server + '/sync',json= json, headers= headers)
                    if responce.status_code != 200:
                        return {"message" : " the server cannot or will not process the request due to something perceived to be a client error"}, 400
                except:
                    json["server"] = second_order_server                
                    response = requests.post(recovery_server + '/addOrder', json= json, headers= headers)

                return order_schema.jsonify(orders), 201
            else:
                return {"message": "This book is currently unavailable"}, 410
        elif responce.status_code == 404:
            return {"message": "This book unavailable"}, 404
        else:
            return {"message": "This book is currently unavailable"}, 410
    except:
        return {"message": "The server is not ready to handle the request"}, 503


@order_server.route("/sync",methods=['PUT'])  
def syncUpDateInfo():
    """
    handle the sync between order servers
    if other order servers update there database 
    the sync update info will be called to infrom this server about this updates
    """
    try:
        order = Orders(request.json['book_id'])
        db.session.add(order)
        db.session.commit()
        return order_schema.jsonify(order), 200
    except:
        return {"message" : " the server cannot or will not process the request due to something perceived to be a client error"}, 400

@catalog_server.before_first_request
def checkAnyUpdates():
    try:
        response = requests.get(recovery_server + '/getOrder/' + this_server)
        order = None

        for newOrders in response.json():
            order = Orders.query.get(newOrders['order_id'])
            if order:
                order.order_id = newOrders['order_id']
                order.book_id = newOrders['book_id']
            else:
                order = Orders(book_id= newOrders['book_id'], order_id= newOrders['order_id'])
                db.session.add(order)
            db.session.commit()
    except:
        print("apple")
        pass

@order_server.errorhandler(404)
def resource_could_not_found(e):
    return jsonify({'error': 404}), 404

@order_server.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'errdor': 405}), 405

if __name__ == "__main__":
    order_server.run(debug = True, port = 2040, host= '0.0.0.0')
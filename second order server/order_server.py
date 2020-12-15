from flask.globals import request
import requests
from server_configuration import *


@order_server.route("/buy/<int:id>", methods=['PUT'])
def buy(id):
    """
    this method response to handle the buy request comes from the fron-end server to be completed the purchase order
    """
    try:
        # check the quanity for this book
        responce = requests.get(
            catalog_server + '/verify_item_in_stock/' + str(id), timeout=(0.3, 2))
        #  if status code 200 and which means there is books at the stock
        # to completed the purchase order send buy request for the catalog server
        if responce.status_code == 200 and responce.json()['quantity'] > 0:
            responce = requests.put(
                catalog_server + '/buy/' + str(id), timeout=(0.3, 5))
            # if the order done (satus code == 204)
            if responce.status_code == 204:
                #  add the order to the databse
                orders = Orders(id)
                db.session.add(orders)
                db.session.commit()
                headers = {'Content-type': 'application/json'}
                json = order_schema.dump(orders)
                try:
                    # try to send sync to 2nd order include book id
                    responce = requests.put(
                        second_order_server + '/sync', json=json, headers=headers, timeout=(0.3, 2))
                    if responce.status_code != 200:
                        return {"message": " the server cannot or will not process the request due to something perceived to be a client error"}, 400
                except:
                    # if 2nd order doesn't respond send it to the recovery server
                    json["server"] = second_order_server
                    response = requests.post(
                        recovery_server + '/addOrder', json=json, headers=headers, timeout=(0.3, 2))

                return order_schema.jsonify(orders), 201
            else:
                return {"message": "This book is currently unavailable"}, 410
        elif responce.status_code == 404:
            return {"message": "This book unavailable"}, 404
        else:
            return {"message": "This book is currently unavailable"}, 410
    except:
        return {"message": "The server is not ready to handle the request"}, 503


@order_server.route("/sync", methods=['PUT'])
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
        return {"message": " the server cannot or will not process the request due to something perceived to be a client error"}, 400


@order_server.before_first_request
def checkAnyUpdates():
    """
    before first request the server check if there is any updates inside the recovery server
    """
    try:
        headers = {'Content-type': 'application/json'}
        json = {'server': this_server}
        # send getOrder to recovery server
        response = requests.get(
            recovery_server + '/getOrder', headers=headers, json=json, timeout=(0.3, 5))
        order = None
        # if there is new order added to database
        for newOrders in response.json():
            order = Orders.query.get(newOrders['order_id'])
            if not order:
                order = Orders(newOrders['book_id'])
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
    order_server.run(debug=True, port=2041, host='0.0.0.0')

from flask import Flask, request, jsonify
import os


app = Flask(__name__)

@app.route('/search/<string:topic>',methods = ['GET'])
def search(topic):
    return {'message':topic}

@app.route('/lookup/<int:id>',methods = ['GET'])
def lookup(id):
    return {'message':id}

@app.route('/buy/<int:id>',methods = ['PUT'])
def buy(id):
    return {'message':id}

@app.errorhandler(404)
def resource_could_not_found(e):
    return jsonify({'error': 404}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 405}), 405

if __name__ == '__main__':
  app.run(debug = True, port = 2309)
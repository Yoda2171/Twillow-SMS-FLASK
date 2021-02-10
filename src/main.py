"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from twilio.rest import Client
from flask import Flask, request, jsonify, url_for

from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap

from models import Queue
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)


_queue = Queue()

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/all', methods=['GET'])
def todos():
    
    usuario = _queue.get_queue()
    return jsonify(usuario),200 
   
    
@app.route('/next', methods=['DELETE'])
def siguente():
   
    usuario = _queue.dequeue()
    return jsonify({"success": "Deleted Complete"}),200


@app.route('/new', methods=['POST'])
def creador():
    

    name = request.json.get("name")
    phone = request.json.get("phone")

    item = {
        "name" : name,
        "phone" : phone
    }   

    if not name :
        return({"msg" : "coloca un nombre"})
    if not phone :
        return({"msg" : "coloca un phone"})

    _queue.enqueue(item)

    return({"msg" : "send complete"})

    


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

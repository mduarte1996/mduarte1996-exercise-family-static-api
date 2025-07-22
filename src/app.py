"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app) 

    
@app.route('/members', methods=['GET'])
def get_all_members():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "Miembro no encontrado"}), 404
    
@app.route('/members', methods=['POST'])
def add_member():
    try:
        member = request.json
        if not member or "first_name" not in member or "age" not in member or "lucky_numbers" not in member:
            return jsonify({"error": "Datos incompletos"}), 400
        jackson_family.add_member(member)
        return jsonify(member), 201
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500
    
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    success = jackson_family.delete_member(member_id)
    if success:
        return jsonify({"done": True}), 200
    else:
        return jsonify({"error": "Miembro no encontrado"}), 404


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

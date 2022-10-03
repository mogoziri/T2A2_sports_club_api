from flask import Blueprint, jsonify, request
from main import db
from main import bcrypt
from models.clients import Client
from schemas.client_schema import client_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

clients = Blueprint("clients", __name__, url_prefix="/clients")


@clients.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_client(id):
    # Only token is not enough to get information about client, the identity needs to be a client or admin
    if get_jwt_identity() != str(id) and get_jwt_identity() != "admin":
        return {
            "error": "You don't have user rights to get information about a client"
        }, 401
    # Search client by id
    client_by_id = Client.query.get(id)
    if not client_by_id:
        return {"error": "Client id not found"}

    result = client_schema.dump(client_by_id)
    return jsonify(result), 200


# Update client's details from the request
@clients.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_client(id):
    # Only token is not enough to update details, the identity needs to be a client
    if get_jwt_identity() != str(id):
        return {"error": "You don't have user rights to update a client"}, 401
    # Get the values from the request and load them with the single schema
    client = Client.query.get(id)
    # Check if we found a client
    if not client:
        return {"error": "Client id not found"}, 404

    # Get the schedule details from the request
    client_fields = client_schema.load(request.json)

    client.username = (client_fields["username"],)
    client.email = (client_fields["email"],)
    client.password = (
        bcrypt.generate_password_hash(client_fields["password"]).decode("utf-8"),
    )
    client.first_name = (client_fields["first_name"],)
    client.last_name = (client_fields["last_name"],)
    client.address = (client_fields["address"],)
    client.phone_number = (client_fields["phone_number"],)
    client.dob = client_fields["dob"]

    db.session.commit()

    return jsonify(client_schema.dump(client)), 201


# Delete a client from the database
@clients.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_client(id):
    # Only token is not enough to delete a client, the identity needs to be an admin
    if get_jwt_identity() != "admin":
        return {"error": "You don't have admin rights to delete a client"}, 401
    # Search client by id (primary key)
    client = Client.query.get(id)
    # Check if we found a client
    if not client:
        return {"error": "Client id not found"}, 404

    # Delete client from the database
    db.session.delete(client)
    db.session.commit()

    return {"message": "Client deleted successfully"}

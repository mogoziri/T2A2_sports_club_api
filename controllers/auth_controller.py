from datetime import timedelta
from flask import Blueprint, request
from main import db
from main import bcrypt
from flask_jwt_extended import create_access_token
from models.clients import Client
from schemas.client_schema import client_schema
from models.admin import Admin
from schemas.admin_schema import admin_schema
from marshmallow.exceptions import ValidationError

auth = Blueprint("auth", __name__, url_prefix="/auth")

# Register a new client
@auth.route("/register", methods=["POST"])
def register_client():
    # Get a client details from the request
    client_fields = client_schema.load(request.json)
    # Find a client by username to check if it is already in the database
    client = Client.query.filter_by(username=client_fields["username"]).first()
    if client:
        return {"error": "Username already exists in database"}

    # Find a client by email to check if it is already in the database
    client = Client.query.filter_by(email=client_fields["email"]).first()
    if client:
        return {"error": "Email already exists in database"}
    # Create client object
    client = Client(
        username=client_fields["username"],
        email=client_fields["email"],
        password=bcrypt.generate_password_hash(client_fields["password"]).decode(
            "utf-8"
        ),
    )

    # Add the client to the database
    db.session.add(client)
    # Save the changes in the database
    db.session.commit()

    # Generate the token setting the identity and expiry time(1 day)
    token = create_access_token(
        identity=str(client.client_id), expires_delta=timedelta(days=1)
    )

    return {"username": client.username, "token": token}, 201


# Login client (POST method)
@auth.route("/login", methods=["POST"])
def login_client():
    # Get username and password from the request
    client_fields = client_schema.load(request.json)
    # Check username and password: user needs to exist, password needs to match
    client = Client.query.filter_by(username=client_fields["username"]).first()
    if not client:
        return {"error": "Invalid username"}

    if not bcrypt.check_password_hash(client.password, client_fields["password"]):
        return {"error": "Invalid password"}

    # Credentials are valid, so generate token and return it to the user

    token = create_access_token(
        identity=str(client.client_id), expires_delta=timedelta(days=1)
    )

    return {"username": client.username, "token": token}, 200


# Login admin (POST method)
@auth.route("/admin/login", methods=["POST"])
def login_admin():
    # Get username and password from the request
    admin_fields = admin_schema.load(request.json)
    # Check username and password: user needs to exist, password needs to match
    admin = Admin.query.filter_by(username=admin_fields["username"]).first()
    if not admin:
        return {"error": "Invalid username"}

    if not bcrypt.check_password_hash(admin.password, admin_fields["password"]):
        return {"error": "Invalid password"}

    # Credentials are valid, so generate token and return it to the user

    token = create_access_token(identity="admin", expires_delta=timedelta(days=1))

    return {"username": admin.username, "token": token}, 200


@auth.errorhandler(ValidationError)
def register_validation_error(error):
    # Print (error.messages)
    return error.messages, 400

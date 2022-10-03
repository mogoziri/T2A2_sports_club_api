from flask import Blueprint, jsonify, request
from main import db
from models.trainers import Trainer
from schemas.trainer_schema import trainer_schema, trainers_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

trainers = Blueprint("trainers", __name__, url_prefix="/trainers")


@trainers.route("/", methods=["GET"])
def get_trainers():
    # Get all trainers from the db
    trainers_list = Trainer.query.all()
    result = trainers_schema.dump(trainers_list)
    return jsonify(result), 200


@trainers.route("/<int:id>", methods=["GET"])
def get_trainer(id):
    # Search trainer by id
    trainer_by_id = Trainer.query.get(id)
    if not trainer_by_id:
        return {"error": "Trainer id not found"}, 404

    result = trainer_schema.dump(trainer_by_id)
    return jsonify(result), 200


# Post a new trainer to the database
@trainers.route("/", methods=["POST"])
# A token is needed for this request
@jwt_required()
def new_trainer():
    # A token is not enough, the identity needs to be an admin
    if get_jwt_identity() != "admin":
        return {"error": "You don't have admin rights to create a new trainer"}, 401
    # Get the values from the request and load them with the single schema
    trainer_fields = trainer_schema.load(request.json)
    # Create a new trainer object
    trainer = Trainer(
        first_name=trainer_fields["first_name"],
        last_name=trainer_fields["last_name"],
        phone_number=trainer_fields["phone_number"],
    )

    db.session.add(trainer)
    # Store in the database and save the changes
    db.session.commit()

    return jsonify(trainer_schema.dump(trainer)), 201


# Update a trainer in the database
@trainers.route("/<int:id>", methods=["PUT"])
# A token is needed for this request
@jwt_required()
def update_trainer():
    # A token is not enough, the identity needs to be an admin
    if get_jwt_identity() != "admin":
        return {"error": "You don't have admin rights to update a trainer"}, 401
    trainer = Trainer.query.get(id)
    # Check if trainer exists in the db
    if not trainer:
        return {"error": "trainer id not found"}, 404
    # Get the values from the request and load them with the single schema
    trainer_fields = trainer_schema.load(request.json)
    # Update a trainer object
    trainer.first_name = trainer_fields["first_name"]
    trainer.last_name = trainer_fields["last_name"]
    trainer.phone_number = trainer_fields["phone_number"]

    # Store in the database and save the changes
    db.session.commit()

    return jsonify(trainer_schema.dump(trainer)), 201


# Delete a trainer
@trainers.route("/<int:id>", methods=["DELETE"])
# A token is needed for this request
@jwt_required()
def delete_trainer(id):
    # Token is not enough, the identity needs to be an admin
    if get_jwt_identity() != "admin":
        return {"error": "You don't have admin rights to create a new trainer"}, 401
    # Search trainer by id (primary key)
    trainer = Trainer.query.get(id)
    # Check if we found a trainer
    if not trainer:
        return {"error": "Trainer id not found"}, 404

    # Delete trainer from db
    db.session.delete(trainer)
    db.session.commit()

    return {"message": "Trainer deleted successfully"}, 200

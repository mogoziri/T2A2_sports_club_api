from flask import Blueprint, jsonify, request
from main import db
from models.trainings import Training
from schemas.training_schema import training_schema, trainings_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

trainings = Blueprint("trainings", __name__, url_prefix="/trainings")


@trainings.route("/", methods=["GET"])
def get_trainings():
    # Get the filtered search from the database
    if request.query_string:
        if request.args.get("training_type"):
            filtered_trainings_list = Training.query.filter_by(
                training_type=request.args.get("training_type")
            )
            result = trainings_schema.dump(filtered_trainings_list)
            return jsonify(result), 200
        else:
            return {"message": "Training type not found exist in the database."}, 404
    # Get all trainings from the database
    trainings_list = Training.query.all()
    result = trainings_schema.dump(trainings_list)
    return jsonify(result), 200


@trainings.route("/<int:id>", methods=["GET"])
def get_training(id):
    # Get the training from the database by id
    training_by_id = Training.query.get(id)
    result = training_schema.dump(training_by_id)
    return jsonify(result), 200


# Post a new training to the database
@trainings.route("/", methods=["POST"])
# A token is needed for this request
@jwt_required()
def new_training():
    # Only token is not enough, the identity needs to be an admin
    if get_jwt_identity() != "admin":
        return {"error": "You don't have admin rights to create a new training"}, 401
    training_fields = training_schema.load(request.json)
    training_new = Training(
        training_type=training_fields["training_type"],
        trainer_id=training_fields["trainer_id"],
    )

    db.session.add(training_new)
    db.session.commit()
    return jsonify(training_schema.dump(training_new)), 201


# Update the training information in the database
@trainings.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_training(id):
    # Token is not enough, the identity needs to be an admin
    if get_jwt_identity() != "admin":
        return {"error": "You don't have admin rights to create a new training"}, 401
    # Find the training in the db by id
    training = Training.query.get(id)
    # Check if training exists in the db
    if not training:
        return {"error": "training id not found"}, 404
    # Get the training details from the request
    training_fields = training_schema.load(request.json)

    training.training_type = training_fields["training_type"]

    db.session.commit()

    return jsonify(training_schema.dump(training)), 200


# Delete a training from the database
@trainings.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_training(id):
    # Only token is not enough to delete a training, the identity needs to be an admin
    if get_jwt_identity() != "admin":
        return {"error": "You don't have admin rights to delete a training"}, 401
    # Search training by id (primary key)
    training = Training.query.get(id)
    # Check if we found a training
    if not training:
        return {"error": "Training id not found"}

    # Delete a training from the database
    db.session.delete(training)
    db.session.commit()

    return {"message": "Training_id deleted successfully"}, 200

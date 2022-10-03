from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import db
from models.room import Room
from models.schedule import Schedule
from models.trainings import Training
from schemas.schedule_schema import schedule_schema, schedules_schema

schedule = Blueprint("schedule", __name__, url_prefix="/schedule")


@schedule.route("/", methods=["GET"])
def get_schedules():
    # Get all schedule items from the db
    schedule_list = Schedule.query.all()
    result = schedules_schema.dump(schedule_list)
    return jsonify(result), 200


@schedule.route("/<int:id>", methods=["GET"])
def get_schedule(id):
    # Get the schedule item from the db by id
    schedule = Schedule.query.get(id)
    if not schedule:
        return {"error": "Schedule id not found"}, 404
    result = schedule_schema.dump(schedule)
    return jsonify(result), 200


# Post a new schedule item to the database
@schedule.route("/", methods=["POST"])
# A token is needed for this request
@jwt_required()
def new_schedule():
    # A token is not enough, the identity needs to be an admin
    if get_jwt_identity() != "admin":
        return {
            "error": "You don't have admin rights to create a new schedule item"
        }, 401
    schedule_fields = schedule_schema.load(request.json)

    if not Training.query.get(schedule_fields["training_id"]):
        return {"error": "Training id not found"}, 400

    if not Room.query.get(schedule_fields["room_id"]):
        return {"error": "Room id not found"}, 400

    schedule_new = Schedule(
        training_id=schedule_fields["training_id"],
        room_id=schedule_fields["room_id"],
        day=schedule_fields["day"],
        start_time=schedule_fields["start_time"],
        finish_time=schedule_fields["finish_time"],
    )

    db.session.add(schedule_new)
    db.session.commit()
    return jsonify(schedule_schema.dump(schedule_new)), 201


@schedule.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_schedule(id):
    # A token is not enough, the identity needs to be an admin
    if get_jwt_identity() != "admin":
        return {"error": "You don't have admin rights to update a schedule"}, 401
    # Find the schedule item in the db by id
    schedule = Schedule.query.get(id)
    # Check if schedule item exists in the db
    if not schedule:
        return {"error": "Schedule id not found"}, 404
    # get the schedule details from the request
    schedule_fields = schedule_schema.load(request.json)

    if not Training.query.get(schedule_fields["training_id"]):
        return {"error": "Training id not found"}, 400

    if not Room.query.get(schedule_fields["room_id"]):
        return {"error": "Room id not found"}, 400

    schedule.training_id = schedule_fields["training_id"]
    schedule.room_id = schedule_fields["room_id"]
    schedule.day = schedule_fields["day"]
    schedule.start_time = schedule_fields["start_time"]
    schedule.finish_time = schedule_fields["finish_time"]

    db.session.commit()

    return jsonify(schedule_schema.dump(schedule)), 200


# Delete a schedule_id from the database
@schedule.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_schedule(id):
    # Only token is not enough to delete a schedule item, the identity needs to be an admin
    if get_jwt_identity() != "admin":
        return {"error": "You don't have admin rights to delete a schedule_id"}, 401
    # Search schedule item by id (primary key)
    schedule = Schedule.query.get(id)
    # Check if we found a schedule item
    if not schedule:
        return {"error": "Schedule id not found"}, 404

    # Delete a schedule_id from the database
    db.session.delete(schedule)
    db.session.commit()

    return {"message": "Schedule_id deleted successfully"}, 200

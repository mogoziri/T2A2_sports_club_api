from flask import Blueprint, jsonify, request
from main import db
from models.clients import Client
from models.room import Room
from models.schedule import Schedule
from models.visit import Visit
from schemas.visit_schema import visit_schema, visits_schema

from flask_jwt_extended import jwt_required, get_jwt_identity

visit = Blueprint("visit", __name__, url_prefix="/visit")


@visit.route("/", methods=["GET"])
# A token is needed for this request
@jwt_required()
def get_visits():
    # Only token is not enough to get information about all clients visits, the identity needs to be an admin
    if get_jwt_identity() != "admin":
        return {
            "error": "You don't have admin rights to get information about  client visits"
        }, 401
    # Get all visit from the db
    visit_list = Visit.query.all()
    result = visits_schema.dump(visit_list)
    return jsonify(result), 200


@visit.route("/<int:id>", methods=["GET"])
# A token is needed for this request
@jwt_required()
def get_visit(id):
    # Only token is not enough to get information about client visits, the identity needs to be a client or admin
    if get_jwt_identity() != str(id) and get_jwt_identity() != "admin":
        return {
            "error": "You don't have user or admin rights to get information about  a client visit"
        }, 401
    # Get the visit from the db by id
    visit_by_id = Visit.query.get(id)
    result = visit_schema.dump(visit_by_id)
    return jsonify(result), 200


# Post a new visit and check if room capacity is allowing it
@visit.route("/", methods=["POST"])
# A token is needed for this request
@jwt_required()
def new_visit():
    # Only token is not enough, the identity needs to be an admin
    if get_jwt_identity() != "admin":
        return {"error": "You don't have admin rights to create a new visit"}, 401
    visit_fields = visit_schema.load(request.json)

    if not Client.query.get(visit_fields["client_id"]):
        return {"error": "Client id not found"}, 400

    if not Schedule.query.get(visit_fields["schedule_id"]):
        return {"error": "Schedule id not found"}, 400

    schedule = Schedule.query.get(visit_fields["schedule_id"])
    # Checking the capacity of the room
    actual_visits_query = Visit.query.filter_by(schedule_id=schedule.schedule_id)
    actual_visits = visits_schema.dump(actual_visits_query)
    room = Room.query.get(schedule.room_id)

    if len(actual_visits) >= room.capacity:
        return {"error": "Room capacity exceeded"}

    visit_new = Visit(
        client_id=visit_fields["client_id"],
        schedule_id=visit_fields["schedule_id"],
    )

    db.session.add(visit_new)
    db.session.commit()
    return jsonify(visit_schema.dump(visit_new)), 201


# Update visit information in the database
@visit.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_visit(id):
    # A token is not enough, the identity needs to be an admin
    if get_jwt_identity() != "admin":
        return {"error": "You don't have admin rights to update a visit"}, 401
    # Find the visit in the db by id
    visit = Visit.query.get(id)
    # Check if visit exists in the db
    if not visit:
        return {"error": "visit id not found"}
    # Get the visit details from the request
    visit_fields = visit_schema.load(request.json)

    if not Client.query.get(visit_fields["client_id"]):
        return {"error": "Client id not found"}, 400

    if not Schedule.query.get(visit_fields["schedule_id"]):
        return {"error": "Schedule id not found"}, 400

    visit.client_id = (visit_fields["client_id"],)
    visit.schedule_id = (visit_fields["schedule_id"],)

    db.session.commit()

    return jsonify(visit_schema.dump(visit)), 201

from main import db


class Room(db.Model):
    # define the tablename in the database
    __tablename__ = "rooms"
    room_id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(), nullable=False)
    capacity = db.Column(db.Integer, default=8)
    schedules = db.relationship("Schedule", backref="room")

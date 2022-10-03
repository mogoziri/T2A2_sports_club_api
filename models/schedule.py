from main import db


class Schedule(db.Model):
    # define the tablename in the database
    __tablename__ = "schedule"
    schedule_id = db.Column(db.Integer, primary_key=True)
    training_id = db.Column(db.Integer, db.ForeignKey("trainings.training_id"))
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.room_id"))
    day = db.Column(db.String())
    start_time = db.Column(db.Time, nullable=False)
    finish_time = db.Column(db.Time, nullable=False)

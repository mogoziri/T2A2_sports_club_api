from main import db


class Training(db.Model):
    # define the tablename in the database
    __tablename__ = "trainings"
    training_id = db.Column(db.Integer, primary_key=True)
    training_type = db.Column(db.String())
    trainer_id = db.Column(db.Integer, db.ForeignKey("trainers.trainer_id"))
    schedules = db.relationship("Schedule", backref="training")

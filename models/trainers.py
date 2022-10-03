from main import db


class Trainer(db.Model):
    # define the tablename in the database as trainers
    __tablename__ = "trainers"
    # setting the columns
    trainer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    phone_number = db.Column(db.String())
    trainings = db.relationship("Training", backref="trainer")

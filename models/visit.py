from main import db
from sqlalchemy.sql import func


class Visit(db.Model):
    # define the tablename in the database
    __tablename__ = "visits"

    visit_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.client_id"))
    schedule_id = db.Column(db.Integer, db.ForeignKey("schedule.schedule_id"))
    visit_timestamp = db.Column(db.DateTime, nullable=False, server_default=func.now())

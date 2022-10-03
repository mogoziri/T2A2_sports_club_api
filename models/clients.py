from main import db


class Client(db.Model):
    # define the tablename in the database as clients
    __tablename__ = "clients"
    # setting the columns
    client_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    address = db.Column(db.String())
    phone_number = db.Column(db.String())
    dob = db.Column(db.String())
    visits = db.relationship("Visit", backref="client")

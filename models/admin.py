from main import db


class Admin(db.Model):
    # define the tablename in the database as admins
    __tablename__ = "admins"
    # setting the columns
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    shift = db.Column(db.String(), default="Weekdays")
    payrate = db.Column(db.Float(), default=27.0)

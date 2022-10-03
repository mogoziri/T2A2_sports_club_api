from datetime import time
from flask import Blueprint
from main import db
from main import bcrypt
from models.trainers import Trainer
from models.trainings import Training
from models.clients import Client
from models.admin import Admin
from models.room import Room
from models.schedule import Schedule
from models.visit import Visit

db_commands = Blueprint("db", __name__)


@db_commands.cli.command("create")
def create_db():
    # Command SQLAlchemy to create all tabeles for all models in the DB
    db.create_all()
    print("Tables created succesfully")


@db_commands.cli.command("drop")
def drop_db():
    # Command SQLAlchemy to drop all tables for all models in the DB
    db.drop_all()
    print("Tables dropped succesfully")


@db_commands.cli.command("seed")
def seed_db():

    admin1 = Admin(
        username="kate",
        password=bcrypt.generate_password_hash("87654321").decode("utf-8"),
    )

    db.session.add(admin1)

    client1 = Client(
        username="Timofey",
        email="timofey@gmail.com",
        password=bcrypt.generate_password_hash("12345678").decode("utf-8"),
        first_name="Timofey",
        last_name="Mogozov",
    )

    db.session.add(client1)

    client2 = Client(
        username="Emi",
        email="emi@gmail.com",
        password=bcrypt.generate_password_hash("password").decode("utf-8"),
        first_name="Emi",
        last_name="Mogozova",
    )

    db.session.add(client2)

    client3 = Client(
        username="Amelia",
        email="amelia@gmail.com",
        password=bcrypt.generate_password_hash("drowssap").decode("utf-8"),
        first_name="Amelia",
        last_name="Tenser",
    )

    db.session.add(client3)

    trainer1 = Trainer(
        first_name="Irina", last_name="Mogozova", phone_number="0400401234"
    )

    db.session.add(trainer1)

    trainer2 = Trainer(first_name="Ivan", last_name="Trenev", phone_number="0506781256")

    db.session.add(trainer2)

    trainer3 = Trainer(
        first_name="Alexander", last_name="Mitchell", phone_number="0506789876"
    )

    db.session.add(trainer3)

    training1 = Training(training_type="Yoga", trainer=trainer2)

    db.session.add(training1)

    training2 = Training(training_type="Contemporary dance", trainer=trainer1)

    db.session.add(training2)

    training3 = Training(training_type="Individual training", trainer=trainer1)

    db.session.add(training3)

    room1 = Room(room_name="Volga", capacity=2)

    db.session.add(room1)

    room2 = Room(room_name="Amazon", capacity=4)

    db.session.add(room2)

    room3 = Room(room_name="Nile", capacity=6)

    db.session.add(room3)

    db.session.commit()

    schedule1 = Schedule(
        training_id=training1.training_id,
        room_id=room1.room_id,
        day="Wednesday",
        start_time=time(hour=14),
        finish_time=time(hour=15),
    )

    db.session.add(schedule1)

    schedule2 = Schedule(
        training_id=training2.training_id,
        room_id=room2.room_id,
        day="Wednesday",
        start_time=time(hour=10),
        finish_time=time(hour=11),
    )

    db.session.add(schedule2)

    visit1 = Visit(client_id=client1.client_id, schedule_id=schedule1.schedule_id)

    db.session.add(visit1)

    visit2 = Visit(client_id=client2.client_id, schedule_id=schedule2.schedule_id)

    db.session.add(visit2)

    visit3 = Visit(client_id=client2.client_id, schedule_id=schedule1.schedule_id)

    db.session.add(visit3)

    db.session.commit()
    print("tables seeded succesfully")

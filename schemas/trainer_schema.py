from main import ma
from marshmallow import fields

from schemas.training_schema import TrainingSchema


class TrainerSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("trainer_id", "first_name", "last_name", "phone_number", "trainings")

    trainings = fields.List(fields.Nested(TrainingSchema, only=("training_type",)))


trainer_schema = TrainerSchema()
trainers_schema = TrainerSchema(many=True)

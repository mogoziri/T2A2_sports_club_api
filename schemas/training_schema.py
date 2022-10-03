from main import ma
from marshmallow import fields


class TrainingSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ["training_id", "training_type", "trainer_id", "trainer"]
        load_only = ["trainer_id"]

    # schema is defined as a string to avoid circular import error
    trainer = fields.Nested(
        "TrainerSchema",
        only=(
            "first_name",
            "last_name",
        ),
    )


# single training schema
training_schema = TrainingSchema()
# multiple schema
trainings_schema = TrainingSchema(many=True)

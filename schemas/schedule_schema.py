from main import ma
from marshmallow import fields
from schemas.training_schema import TrainingSchema
from schemas.room_schema import RoomSchema


class ScheduleSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = [
            "schedule_id",
            "room_id",
            "training_id",
            "day",
            "start_time",
            "finish_time",
            "training",
            "room",
        ]
        load_only = ["room_id", "training_id"]

    training = fields.Nested(TrainingSchema, only=("training_type",))
    room = fields.Nested(RoomSchema, only=("room_name",))


schedule_schema = ScheduleSchema()
schedules_schema = ScheduleSchema(many=True)

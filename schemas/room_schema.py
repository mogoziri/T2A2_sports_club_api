from main import ma


class RoomSchema(ma.Schema):
    class Meta:
        fields = ["room_id", "room_name", "capacity"]


room_schema = RoomSchema()

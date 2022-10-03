from main import ma
from marshmallow import fields

class VisitSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ["visit_id", "client_id", "schedule_id", "client"]
        load_only = ["client_id"]
    client = fields.Nested("ClientSchema", only=("first_name","last_name",))
    

visit_schema = VisitSchema()
visits_schema = VisitSchema(many=True)

from main import ma
from marshmallow.validate import Length


class ClientSchema(ma.Schema):
    class Meta:
        fields = (
            "client_id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "address",
            "phone_number",
            "dob",
        )

    # add validation to password
    password = ma.String(validate=Length(min=8))


client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)

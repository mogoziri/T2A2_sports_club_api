from main import ma
from marshmallow.validate import Length


class AdminSchema(ma.Schema):
    class Meta:
        fields = (
            "admin_id",
            "username",
            "password",
            "first_name",
            "last_name",
            "shift",
            "payrate",
        )

    # add validation to password
    password = ma.String(validate=Length(min=8))


# just the single schema for log in purposes
admin_schema = AdminSchema()

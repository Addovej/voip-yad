from marshmallow import fields
from marshmallow import Schema


class BaseModelSchema(Schema):
    id = fields.Integer()
    created = fields.DateTime()
    modified = fields.DateTime()


class LoginUserSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)


class UpdateUserSchema(Schema):
    first_name = fields.String()
    last_name = fields.String()
    ya_disc_token = fields.String()


class CreateUserSchema(LoginUserSchema, UpdateUserSchema):
    pass


class UserSchema(BaseModelSchema, UpdateUserSchema):
    email = fields.String()

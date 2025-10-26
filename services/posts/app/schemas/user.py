from marshmallow import Schema, fields



class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()

user_schema = UserSchema()
from marshmallow import fields, Schema
from app.schemas.user import UserSchema


class PostSchema(Schema):
    id = fields.Int(required=True)
    description = fields.Str(required=True)
    image_urls = fields.List(fields.Str(), required=True)
    created_at = fields.DateTime(required=True)
    user = fields.Nested(UserSchema, required=True)
    likes_count = fields.Int(required=True)
    is_liked = fields.Boolean(required=True)
    is_owner = fields.Boolean(required=True)

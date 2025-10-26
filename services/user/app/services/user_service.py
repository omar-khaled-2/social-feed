
from flask import Blueprint , jsonify , current_app
from app.models.user import User
from app.db import db
user_blueprint = Blueprint('user', __name__)
from flask_jwt_extended import get_jwt_identity,jwt_required
from app.schemas.user_schema import CreateUserSchema

def create_user(create_user:CreateUserSchema):
    username = create_user.username
    password = create_user.password
    user = User()
    user.username = username
    user.set_password(password=password)
    db.session.add(user)
    return user

def get_user(id:int):
    user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one()
    return user
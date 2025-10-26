from flask import Blueprint , jsonify , current_app
from app.models.user import User
from app.db import db
from flask_jwt_extended import get_jwt_identity,jwt_required
from app.schemas.user_schema import user_schema
from app.services.user_service import create_user,get_user
from app.schemas.user_schema import CreateUserSchema
from app.utils import api_token_required

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route("/", methods=["GET"])
@jwt_required(locations=["headers"])
def get_current_user():
    user_id = get_jwt_identity() 
    user = get_user(user_id)
    data = CreateUserSchema(user)
    return jsonify(data), 200

@user_blueprint.route("/", methods=["POST"])
@api_token_required()
def create_user():
    user_id = get_jwt_identity() 
    user = get_user(user_id)
    data = CreateUserSchema(user)
    return jsonify(data), 200




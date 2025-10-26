from flask import Blueprint, request , jsonify
from app.models.user import User
from app.db import db
auth_blueprint = Blueprint('user', __name__)
from flask_jwt_extended import create_access_token



@auth_blueprint.route("/register", methods=["POST"])
def register():
    body = request.get_json()
    username = body.get("username")
    password = body.get("password")

    user = User(username=username)
    user.set_password(password)

 
    db.session.add(user)
    db.session.commit()


    return jsonify({"message": "User registered successfully"}), 201


@auth_blueprint.route("/login", methods=["POST"])
def login():
    body = request.get_json()
    username = body.get("username")
    password = body.get("password")

    query = db.select(User).filter_by(username=username)

    user = db.session.execute(query).scalar_one_or_none()

    if not user:
        return jsonify({"message": "Invalid username"}), 401

    if not user.check_password(password):
        return jsonify({"message": "Invalid password"}), 401
    
    access_token = create_access_token(identity=str(user.id))

    return jsonify({"access_token": access_token}), 200


from flask import Flask
from app.controllers.auth_controller import auth_blueprint
from app.db import db
from flask_jwt_extended import JWTManager
from app.config import Config

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.register_blueprint(auth_blueprint)
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
    jwt.init_app(app)
    db.init_app(app)
    return app



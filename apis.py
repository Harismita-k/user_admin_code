from flask import Flask,jsonify
from todo_api import todo_bp
from datetime import timedelta
from flask_jwt_extended import JWTManager
from todo_api import auth_bp
from db import engine, Base
from werkzeug.exceptions import HTTPException

def create_app():
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = "super-secret-key"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)

    app.register_blueprint(todo_bp)
    app.register_blueprint(auth_bp)

    #Base.metadata.create_all(engine)
    
    jwt = JWTManager(app)

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e,HTTPException):
            return e

    return app


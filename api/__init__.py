
from flask import Flask
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("api/Key.json")
firebase_admin.initialize_app(cred)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "123456"

    from .userAPI import userAPI

    app.register_blueprint(userAPI)

    return app
from flask import Flask, jsonify
import os

from src.auth import auth
from src.books import books
from src.shelves import shelves
from src.database import Base, DatabaseConnection
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    # app.config['CORS_HEADERS'] = 'Content-Type'

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET KEY"),
            SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:@localhost:3306/test',
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
        )
    else:
        app.config.from_mapping(test_config)

    @app.get("/")
    def index():
        return 'Hello world!'

    @app.get("/hello")
    def sayHello():
        return jsonify({"message": "Hello world"})

    db_connection = DatabaseConnection.get_instance()
    db = db_connection.db
    db.app = app
    db.init_app(app)

    app.app_context().push()
    Base.prepare(db.engine, reflect=True)
    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(books)
    app.register_blueprint(shelves)

    return app

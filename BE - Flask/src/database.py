from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.ext.automap import automap_base


class DatabaseConnection:
    __instance = None

    @staticmethod
    def get_instance():
        if DatabaseConnection.__instance is None:
            DatabaseConnection()
        return DatabaseConnection.__instance

    def __init__(self):
        if DatabaseConnection.__instance is not None:
            raise Exception("Only one instance of the database connection is allowed.")
        else:
            DatabaseConnection.__instance = self
            self.db = SQLAlchemy()


db_connection = DatabaseConnection.get_instance()
db = db_connection.db
Base = automap_base()


class User(db.Model):
    # add first name, last name, age
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    shelves = db.relationship('Shelf', backref='user', lazy=True)

    def __repr__(self) -> str:
        return 'User>>> {self.username}'


class Shelf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)

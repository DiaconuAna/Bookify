import pandas as pd
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select, and_
from src.database import Base, DatabaseConnection
from src.database import User, Shelf, Base, DatabaseConnection

db_connection = DatabaseConnection.get_instance()
db = db_connection.db


def getBookById_aux(id):
    BooksTable = Base.classes.books
    get_statement = select(BooksTable).where(BooksTable.Id == id)
    result = db.session.execute(get_statement)
    book = ''
    for row in result:
        if row.books.categories == "No category available":
            category = row.books.categories
        else:
            category = row.books.categories[2:-2]
        book = {'id': row.books.Id,
                'title': row.books.Title,
                'author': row.books.authors[2:-2],
                'image': row.books.image,
                'genre': category,
                }
    return book

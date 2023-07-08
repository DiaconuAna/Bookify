from flask import Blueprint, request, jsonify
from sqlalchemy import select

from src.constants.http_status_codes import HTTP_201_CREATED
from src.database import User, Shelf, Base, DatabaseConnection
from src.utils import getBookById_aux

import random

shelves = Blueprint("shelves", __name__, url_prefix='/api/shelf')
db_connection = DatabaseConnection.get_instance()
db = db_connection.db


def get_shelfId(shelves, shelf_name):
    shelf_id = -1
    for shelf in shelves:
        if shelf['name'] == shelf_name:
            shelf_id = shelf['id']
            break
    return shelf_id


def get_shelves(user_id):
    shelves = Shelf.query.filter_by(user_id=user_id).all()
    result = []
    for shelf in shelves:
        result.append({'id': shelf.id, 'name': shelf.name})
    return result


def getUserBooks(username):
    user_id = User.query.filter_by(username=username).first().id
    shelves = get_shelves(user_id)
    book_ids = []
    ShelvedBooksTable = Base.classes.shelvedbooks
    for shelf in shelves:
        booksQuery = select(ShelvedBooksTable).where(ShelvedBooksTable.ShelfId == shelf['id'])
        books = db.session.execute(booksQuery)
        for row in books:
            book = getBookById_aux(row.shelvedbooks.BookId)
            book['shelf'] = shelf['name']
            book_ids.append(book)
    # print(book_ids)
    return book_ids


@shelves.get('/all_books')
def get_all_user_books():
    return getUserBooks(request.args['username'])


def get_books_from_shelf(user_id, shelf_name):
    shelf_id = get_shelfId(get_shelves(user_id), shelf_name)
    ShelvedBooksTable = Base.classes.shelvedbooks
    booksQuery = select(ShelvedBooksTable).where(ShelvedBooksTable.ShelfId == shelf_id)
    books = db.session.execute(booksQuery)
    result = []
    for row in books:
        book = getBookById_aux(row.shelvedbooks.BookId)
        result.append(book)
    print(result)
    return result


@shelves.get('/books')
def get_shelves_books():
    args = request.args
    user_id = args['user_id']
    shelf_name = args['shelf']
    return get_books_from_shelf(user_id, shelf_name)


@shelves.get("/main_page")
def get_main_page_shelf_books():
    args = request.args
    username = args['username']
    user = User.query.filter_by(username=username).first()
    user_id = user.id

    result = {}
    # read
    books = get_books_from_shelf(user_id, "Read")
    if len(books) > 5:
        books = random.sample(books, 5)
    result['read'] = books

    # to read
    books = get_books_from_shelf(user_id, "To Read")
    if len(books) > 5:
        books = random.sample(books, 5)
    result['to_read'] = books

   # currently reading
    books = get_books_from_shelf(user_id, "Currently Reading")
    if len(books) > 5:
        books = random.sample(books, 5)
    result['currently_reading'] = books

    return jsonify({"books": result})


@shelves.post('/shelf_book')
def addBookToShelf():
    ShelvedBooksTable = Base.classes.shelvedbooks
    username = request.json['username']
    print(username)
    book_id = request.json['book_id']
    shelf_name = request.json['shelf_name']
    # find shelf id for given user
    user = User.query.filter_by(username=username).first()
    shelves = Shelf.query.filter_by(user_id=user.id).all()
    shelves_ids = [s.id for s in shelves]
    shelf = [s for s in shelves if s.name == shelf_name][0]
    # find all other occurrences of the book_id for the current user_id and delete them => shelves are mutually
    # exclusive
    delete_query = db.session.query(ShelvedBooksTable)
    delete_query = delete_query.filter(ShelvedBooksTable.BookId == book_id)
    delete_query = delete_query.filter(ShelvedBooksTable.ShelfId.in_(shelves_ids))
    delete_query.delete()
    db.session.commit()

    new_row = ShelvedBooksTable(BookId=book_id, ShelfId=shelf.id)
    db.session.add(new_row)
    db.session.commit()

    return jsonify({'message': 'Shelf entry created'}), HTTP_201_CREATED

from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash  # used to encrypt the user password
import validators
from src.database import User, Shelf, DatabaseConnection
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK, \
    HTTP_401_UNAUTHORIZED
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth = Blueprint("auth", __name__, url_prefix='/api/auth')
db_connection = DatabaseConnection.get_instance()
db = db_connection.db

@auth.post('/register')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if len(password) < 6:
        return jsonify({'error': 'Password must have more than 6 characters'}), HTTP_400_BAD_REQUEST

    # check username is alphanumeric
    if len(username) < 3:
        return jsonify({'error': 'Username is too short'}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({'error': 'Username should be alphanumeric with no spaces'}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': 'Email is not valid'}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': "Email is taken"}), HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': "Username is taken"}), HTTP_409_CONFLICT

    hashed_password = generate_password_hash(password)

    user = User(username=username, password=hashed_password, email=email)
    db.session.add(user)
    db.session.commit()

    # upon user creation add the 3 default shelves - to-read, read, currently-reading
    to_read_shelf = Shelf(name='To Read', user_id=user.id)
    currently_reading = Shelf(name='Currently Reading', user_id=user.id)
    read_shelf = Shelf(name='Read', user_id=user.id)
    db.session.add(to_read_shelf)
    db.session.add(currently_reading)
    db.session.add(read_shelf)
    db.session.commit()

    return jsonify({'message': 'User created', 'user': {
        'username': username,
        'email': email
    }}), HTTP_201_CREATED


@auth.post('/login')
def login():
    username = request.json.get('username', '')
    password = request.json.get('password', '')

    user = User.query.filter_by(username=username).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify({
                'user': {
                    'refresh': refresh,
                    'access': access,
                    'username': user.username,
                    'email': user.email
                }

            }), HTTP_200_OK

    return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED


@auth.get('/me')
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        'username': user.username,
        'email': user.email
    }), HTTP_200_OK


@auth.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        'access': access
    }), HTTP_200_OK


def getUserId(username):
    user = User.query.filter_by(username=username).first()
    return user.id

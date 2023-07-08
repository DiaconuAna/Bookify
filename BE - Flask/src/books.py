import pandas as pd
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select, and_

from src.shelves import getUserBooks
from src.datasets.review_sentiment_analysis.review_analysis import formConcepts, analyseText
from src.auth import getUserId
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from src.database import Base, DatabaseConnection
from src.datasets.operations.search_engine import preprocessBooksDataset, findBookByCriteria
from src.datasets.recommendations.keyword_recommender import description_recommender, text_to_keywords
from src.datasets.recommendations.user_profile_recommendations import sentiment_profile

books = Blueprint("books", __name__, url_prefix='/api/books')

books_df = preprocessBooksDataset()
db_connection = DatabaseConnection.get_instance()
db = db_connection.db

'''
Miscellaneous
'''


def get_book_ratings(title):
    RatingsTable = Base.classes.ratings
    ratingsQuery = select(RatingsTable).where(RatingsTable.Title == title)
    res = db.session.execute(ratingsQuery)
    review_list = []

    for row in res:
        review = getReview(row)
        review_list.append(review)

    return review_list


def get_descr_book(title):
    BooksTable = Base.classes.books
    get_statement = select(BooksTable).where(BooksTable.Title == title)
    result = db.session.execute(get_statement)
    book = ''
    for row in result:
        book = {'id': row.books.Id,
                'title': row.books.Title,
                'author': row.books.authors[2:-2].replace("'", ""),
                'image': row.books.image,
                'genre': row.books.categories[2:-2],
                }
    return book


def getReview(res):
    return {
        'id': res.ratings.RatingId,
        'user_id': res.ratings.User_id,
        'profile_name': res.ratings.profileName,
        'score': res.ratings.score,
        'review_summary': res.ratings.reviewsummary,
        'review_text': res.ratings.reviewtext,
        'showPolarity': False
    }


def get_book(res):
    keywords = []
    if res.books.Keywords != "":
        keywords = res.books.Keywords[1:-1].replace("'", "").replace(" ", "")
    if res.books.categories == "No category available":
        category = res.books.categories
    else:
        category = res.books.categories[2:-2]
    res.books.categories = category
    res.books.authors = res.books.authors[2:-2]
    res.books.Keywords = keywords

    return {'id': res.books.Id,
            'title': res.books.Title,
            'description': res.books.description,
            'authors': res.books.authors,
            'image': res.books.image,
            'publisher': res.books.publisher,
            'publishedDate': res.books.publishedDate,
            'categories': res.books.categories,
            'ratingsCount': res.books.ratingsCount,
            'ratingsAverage': res.books.ratingsAverage,
            'keywords': res.books.Keywords
            }


def update_book_rating(title):
    BooksTable = Base.classes.books
    RatingsTable = Base.classes.ratings
    ratings_query = select(RatingsTable.score).where(RatingsTable.Title == title)
    ratings = [r[0] for r in db.session.execute(ratings_query)]
    ratings_count = len(ratings)
    ratings_average = sum(ratings) / ratings_count if ratings_count > 0 else 0
    print(f"Book {title} has {ratings_count} reviews")
    db.session.query(BooksTable).filter(
        BooksTable.Title == title
    ).update({
        BooksTable.ratingsCount: ratings_count,
        BooksTable.ratingsAverage: ratings_average
    })
    db.session.commit()


def get_book_details_by_title(title):
    BooksTable = Base.classes.books
    get_statement = select(BooksTable).where(BooksTable.Title == title)
    result = db.session.execute(get_statement)
    book = ''
    for row in result:
        update_book_rating(row.books.Title)
        book = get_book(row)
    return book


def bookKeywords(book_id):
    BooksTable = Base.classes.books
    current_book = db.session.query(BooksTable).filter(BooksTable.Id == book_id).all()
    for row in current_book:
        if row.description == 'No description available':
            keywords = ''
        else:
            keywords = text_to_keywords(row.description)
        db.session.query(BooksTable).filter(BooksTable.Id == book_id).update({
            BooksTable.Keywords: str(keywords)
        })
        db.session.commit()
        print("Keywords for " + BooksTable.Title + " : " + str(keywords))


def get_user_profile_ratings(username):
    RatingsTable = Base.classes.ratings
    ratingsQuery = select(RatingsTable).where(RatingsTable.profileName == username)
    res = db.session.execute(ratingsQuery)
    review_list = []
    for row in res:
        review = {
            'rating': row.ratings.score,
            'title': row.ratings.Title,
        }
        review_list.append(review)
    return review_list


def populate_rating_emotion(id):
    RatingsTable = Base.classes.ratings
    current_rating = db.session.query(RatingsTable).filter(RatingsTable.RatingId == id).all()
    polarity = 0
    sentiments = ""

    for row in current_rating:
        if row.Polarity == 0 or row.Polarity is None:
            concepts = formConcepts()
            text = row.reviewtext
            results = analyseText(concepts, text)
            db.session.query(RatingsTable).filter(
                RatingsTable.RatingId == id
            ).update({
                RatingsTable.Polarity: results[1],
                RatingsTable.Sentiments: str(results[0])
            })

            db.session.commit()
        polarity = row.Polarity
        sentiments = row.Sentiments

    return {"polarity": polarity, "sentiments": sentiments}


'''
Books
'''


@books.get('/get_book_id')
@jwt_required()
def getBookById():
    args = request.args
    BooksTable = Base.classes.books
    get_statement = select(BooksTable).where(BooksTable.Id == args['id'])
    result = db.session.execute(get_statement)
    book = ''
    for row in result:
        book = {'id': row.books.Id,
                'title': row.books.Title,
                'description': row.books.description,
                'authors': row.books.authors[2:-2],
                'image': row.books.image,
                'publisher': row.books.publisher,
                'publishedDate': row.books.publishedDate,
                'categories': row.books.categories[2:-2],
                'ratingsCount': row.books.ratingsCount,
                'ratingsAverage': row.books.ratingsAverage,
                }
    return book


@books.get('/all')
@jwt_required()
def get_all():
    current_user = get_jwt_identity()
    if current_user is not None:
        BooksTable = Base.classes.books
        get_statement = select(BooksTable).where(BooksTable.publishedDate == 1996)
        results = db.session.execute(get_statement)
        data = []
        for row in results:
            data.append({
                'id': row.books.Id,
                'title': row.books.Title,
                'description': row.books.description
            })
        return jsonify({"books": data})
    else:
        return []


@books.get('/get_reviews')
@jwt_required()
def getReviews():
    args = request.args
    return get_book_ratings(args['title'])


@books.get('/get_book')
@jwt_required()
def getBook():
    args = request.args
    return get_book_details_by_title(args['title'])


@books.get('/get_author')
@jwt_required()
def getBooksByAuthor():
    args = request.args
    BooksTable = Base.classes.books
    get_statement = select(BooksTable).where(BooksTable.authors == '[\'' + args['author'] + '\']')
    result = db.session.execute(get_statement)
    books = []
    for row in result:
        book = get_book(row)
        books.append(book)
    return books


@books.get('/search_detailed')
@jwt_required()
def searchDetailed():
    args = request.args
    page = int(args['page'])
    size = int(args['size'])
    criteria = args['criteria']

    match criteria:
        case "title":
            search_results = findBookByCriteria(books_df, 'title', args['title'])
        case "author":
            search_results = findBookByCriteria(books_df, 'author', args['author'])
        case "genre":
            search_results = findBookByCriteria(books_df, 'genre', args['genre'])
        case _:
            return jsonify({'error': 'Search criteria does not exist'}), HTTP_400_BAD_REQUEST

    search_results = search_results[(page - 1) * size:(page - 1) * size + size - 1]
    return jsonify({"titles": search_results})  # should return more metadata to build a proper list element


@books.get('/search_books')
@jwt_required()
def searchBooks():
    args = request.args
    BooksTable = Base.classes.books
    search_results = []
    query = select(BooksTable).where(BooksTable.Title.like(args['title'] + '%')).limit(7)
    results = db.session.execute(query)
    for row in results:
        book = {'id': row.books.Id,
                'title': row.books.Title,
                }
        search_results.append(book)

    return jsonify({"titles": search_results})


@books.get("/sentiments")
def bookSentiments():
    args = request.args
    books_df = pd.read_csv('src/datasets/emotions/book_emotions.csv')
    selectedBook = books_df[books_df['title'] == args['title'] + "\n"]
    book_sentiments = selectedBook['sentiments'].tolist()
    return jsonify({"sentiments": book_sentiments})


@books.get("/keywords")
def populateKeywordColumn():
    BooksTable = Base.classes.books
    query = select(BooksTable.Id)
    results = db.session.execute(query)
    for row in results:
        bookKeywords(row.Id)


@books.get("book_keywords")
@jwt_required()
def getBookKeywords():
    args = request.args
    BooksTable = Base.classes.books
    current_book = db.session.query(BooksTable).filter(BooksTable.Title == args['title']).all()

    keywords = []
    for row in current_book:
        if row.Keywords != "":
            keywords = row.Keywords

    return jsonify({"keywords": keywords})


"""
Ratings
"""


@books.post("/add_rating")
@jwt_required()
def addBookRating():
    RatingsTable = Base.classes.ratings
    dto = request.get_json()
    new_row = RatingsTable(Id=0, Title=dto['title'], User_id=getUserId(dto['username']), profileName=dto['username'],
                           score=dto['rating'], reviewsummary=dto['summary'], reviewtext=dto['review'], Price=0)
    db.session.add(new_row)
    db.session.commit()
    return jsonify({'message': 'Rating entry created'}), HTTP_201_CREATED


@books.get("/user_reviews_book")
@jwt_required()
def getUserBookRatings():
    RatingsTable = Base.classes.ratings
    args = request.args
    ratingsQuery = select(RatingsTable).where(
        and_(RatingsTable.profileName == args['username'], RatingsTable.Title == args['title']))
    res = db.session.execute(ratingsQuery)
    review_list = []
    for row in res:
        review = {
            'id': row.ratings.RatingId,
            'user_id': row.ratings.User_id,
            'profile_name': row.ratings.profileName,
            'score': row.ratings.score,
            'review_summary': row.ratings.reviewsummary,
            'review_text': row.ratings.reviewtext,
            'showPolarity': False
        }
        review_list.append(review)

    return review_list


@books.get("/rating_polarity")
@jwt_required()
def getRatingPolarityAndSentiments():
    args = request.args
    rating_id = args['id']
    return jsonify(populate_rating_emotion(rating_id))


"""
Recommendations
"""


def getKeywordList(criteria, text):
    if criteria == "keyword":
        text = text.split(',')
        return [t.strip() for t in text]
    elif criteria == "text":
        return text_to_keywords(text)


def get_description_recs_keywords(keyword_list, top_rec):
    recommendations = description_recommender(keyword_list, int(top_rec))
    results = []
    for rec in recommendations:
        book = get_descr_book(rec[0].strip())
        results.append(book)
    return jsonify({"recommendations": results})


@books.get('/descriptionRec')
@jwt_required()
def getDescriptionRecommendations():
    args = request.args
    top = 10
    if 'top' in request.args:
        top = args['top']
    criteria = args['criteria']  # text or keywords
    return get_description_recs_keywords(getKeywordList(criteria, args['text']), top)


@books.get('/profileRec')
@jwt_required()
def getProfileRecommendations():
    args = request.args
    if not getUserBooks(args['username']):
        return jsonify({"recommendations": {"books": [], "sentiments": []}})
    else:
        profile = get_user_profile_ratings(args['username'])
        recommendations = sentiment_profile(profile)
        return jsonify({"recommendations": recommendations})

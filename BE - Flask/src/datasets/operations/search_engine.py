import json

import dask.dataframe as ddf
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import numpy as np


def preprocessBooksDataset():
    books_df = ddf.read_csv("src\\datasets\\books_data.csv", dtype={'Id': 'object'})
    # remove books whose title, description or category have null values
    books_df = books_df.dropna(subset=['description', 'Title', 'categories'])
    books_df.authors = books_df.authors.fillna('none')
    books_df.image = books_df.image.fillna(
        'https://upload.wikimedia.org/wikipedia/commons/b/b9/No_Cover.jpg?20090511140841')

    books_df = books_df.drop(["infoLink", "previewLink"], axis=1).persist()
    books_df['mod_title'] = books_df['Title'].str.replace("[^a-zA-Z0-9 ]", "", regex=True)
    books_df["mod_title"] = books_df["mod_title"].str.lower()
    books_df["mod_title"] = books_df["mod_title"].str.replace("\s+", " ", regex=True)

    books_df['mod_author'] = books_df['authors'].str.replace("[^a-zA-Z0-9 ]", "", regex=True)
    books_df["mod_author"] = books_df["mod_author"].str.lower()
    books_df["mod_author"] = books_df["mod_author"].str.replace("\s+", " ", regex=True)

    books_df['mod_genre'] = books_df['categories'].str.replace("[^a-zA-Z0-9 ]", "", regex=True)
    books_df["mod_genre"] = books_df["mod_genre"].str.lower()
    books_df["mod_genre"] = books_df["mod_genre"].str.replace("\s+", " ", regex=True)

    return books_df.compute()


def findBookByCriteria(books_df, criteria, search_text):
    processed = re.sub("[^a-zA-Z0-9 ]", "", search_text.lower())
    vectorizer = TfidfVectorizer()

    match criteria:
        case "title":
            tfidf = vectorizer.fit_transform(books_df["mod_title"])
        case "author":
            tfidf = vectorizer.fit_transform(books_df["mod_author"])
        case "genre":
            tfidf = vectorizer.fit_transform(books_df["mod_genre"])

    similarity_vec = vectorizer.transform([processed])
    similarity = cosine_similarity(similarity_vec, tfidf).flatten()

    results = []
    for i in similarity.argsort()[-100:][::-1]:  # return it paginated?
        print(i)
        book_object = {
            "id": str(i),
            "title": books_df['Title'].iloc[i],
            "genre": books_df['categories'].iloc[i][2:-2],
            "author": books_df['authors'].iloc[i][2:-2],
            "image": books_df['image'].iloc[i]
        }
        results.append(book_object)
    return results

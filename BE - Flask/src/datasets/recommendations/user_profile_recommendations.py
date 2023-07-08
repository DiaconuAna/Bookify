import difflib
from itertools import islice

import pandas as pd


def sentiment_profile(user_profile_books):
    # step 1: create the profile

    user_book_ratings = pd.DataFrame(user_profile_books)
    books_df = pd.read_csv('src/datasets/emotions/book_emotions.csv')
    books_sentiment_df = pd.read_csv('src/datasets/emotions/book_emotions_detailed.csv')

    # add the book id from the sentiment books df
    # filter out the rows containing the input book's title
    # merge the subset with the input dataframe
    # drop unnecessary columns to save memory space

    books_df['title'] = books_df['title'].replace('\n', '', regex=True)
    user_book_ids = books_df[books_df['title'].isin(user_book_ratings['title'])]
    user_book_ratings = pd.merge(user_book_ids, user_book_ratings)
    user_book_ratings = user_book_ratings.drop(['sentiments', 'polarity'], axis=1)
    user_book_ratings.rename(columns={'Unnamed: 0': 'bookId'}, inplace=True)

    # step 2: learn user profile
    # reset the index to default, drop the existing index
    user_sentiments_df = books_sentiment_df[books_sentiment_df.bookId.isin(user_book_ratings.bookId)]
    user_sentiments_df.reset_index(drop=True, inplace=True)

    user_sentiments_df.drop(['Unnamed: 0', 'bookId', 'title', 'sentiments', 'polarity'], axis=1, inplace=True)

    # step 3 - build user profile
    # turn each sentiment into a weight by multiplying the ratings by the books table
    # dot product of transpose of sentiment_df by ratings

    user_profile = user_sentiments_df.T.dot(user_book_ratings.rating)
    user_profile_sorted = user_profile.sort_values(ascending=False)
    top_sentiments = []
    for index, value in islice(user_profile_sorted.items(), 5):
        sentiment = {'sentiment': index, 'weight': round(value, 2)}
        top_sentiments.append(sentiment)

    # the user profile consists of the weights of his preferences
    # edit the original books_df to contain all books with sentiment columns
    books_sentiment_df = books_sentiment_df.set_index(books_sentiment_df.bookId)

    # delete the irrelevant columns
    books_sentiment_df.drop(['Unnamed: 0', 'bookId', 'title', 'sentiments', 'polarity'], axis=1, inplace=True)

    # take the weighted average of every book based on his profile and recommend top 20 books
    recommendation_table_df = (books_sentiment_df.dot(user_profile)) / user_profile.sum()
    # sort it in descending order
    recommendation_table_df.sort_values(ascending=False, inplace=True)

    # get the list of indices
    books_to_delete = user_book_ratings.bookId.tolist()
    books_df = books_df[~books_df['Unnamed: 0'].isin(books_to_delete)]
    copy = books_df.copy(deep=True)
    copy = copy.set_index('Unnamed: 0', drop=True)
    top_20 = recommendation_table_df.index[:20].tolist()
    recommended_books = []
    for index in top_20:
        recommended_books.append({"id": index, "title": copy.loc[index, 'title'], "sentiments": copy.loc[index, 'sentiments'][1:-1]})

    return {"books": recommended_books, "sentiments": top_sentiments }


def isBookRelevant(book_emotions, user_emotions):
    common_emotions = set(book_emotions) & set(user_emotions)
    emotion_count = len(common_emotions)
    print(emotion_count)
    if emotion_count == 5:
        print('OK')
        return True
    else:
        print('Not OK')
        return False


def evaluateSentiments(user_profile_books):
    result = sentiment_profile(user_profile_books)
    recommended_books = result["books"]
    titles = [r['title'] for  r in recommended_books]
    emotions = result["sentiments"]
    print(emotions)
    sentiment_list = [s['sentiment'] for s in emotions]
    print('******')
    print(sentiment_list)
    print('******')

    relevant_books = []
    df = pd.read_csv('src/datasets/emotions/book_emotions_detailed.csv')

    for book in titles:
        book_emotions = df.loc[df['title'] == book+"\n", 'sentiments'].values[0]

        experiment = book_emotions.split(',')
        experiment[0] = experiment[0][1:]
        experiment[-1] = experiment[-1][:-1]

        if isBookRelevant(experiment, sentiment_list):
            relevant_books.append(book)

    print(len(relevant_books))
    true_positives = len(set(titles) & set(relevant_books))
    false_positives = len(set(titles) - set(relevant_books))
    false_negatives = len(set(relevant_books) - set(titles))

    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)
    F1 = 2 * (precision * recall) / (precision + recall)

    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1: ", F1)


if __name__ == "__main__":
    user_profile_books = [
        # {'title': 'Dr. Seuss: American Icon', 'rating': 4.5},
        # {'title': 'Alaska Sourdough', 'rating': 2.0},
        {'title': 'The Enchanted Wood and Other Tales from Finland:', 'rating': 4.0},
        {'title': 'Requiem for a Wren', 'rating': 2.0},
        # {'title': 'Never Again Once More', 'rating': 3.5},
        {'title': 'The Tragedy of the Korosko (Collected Works of Sir Arthur Conan Doyle)', 'rating': 1.0},
        {'title': 'Resurrection Day', 'rating': 2.0},
        {'title': 'Matilda (French Edition)', 'rating': 1.0},
        # {'title': 'Scotland: A Concise History', 'rating': 5.0},
        # {'title': 'Star girl', 'rating': 4},
        # {'title': 'The Courage To Choose (W.I.T.C.H. No.15)', 'rating': 2.0},
        {'title': 'The Abbots Gibbet (Knights Templar Mysteries (Avon))', 'rating': 4.0},
        # {'title': 'Erotica Vampirica', 'rating': 2.0},
        # {'title': 'Sure of You', 'rating': 5.0},
        # {'title': 'Hangin with Bugs', 'rating': 4.0},
        {'title': 'The Pacific', 'rating': 4.0},
        {'title': 'Band of Brothers', 'rating': 5.0},
        {'title': 'The Last Kingdom (The Saxon Chronicles Series #1)', 'rating': 3.0},
        {'title': 'The Pale Horseman (The Saxon Chronicles Series #2)', 'rating': 2.0},
        {'title': 'Mom and Dad and I Are Having a Baby', 'rating': 4.0},
        {'title': 'Emily of New moon,', 'rating': 5.0},
        {'title': 'Dragonhenge', 'rating': 5.0},
        {'title': 'The Order War (Recluce series, Book 4)', 'rating': 5.0},
        {'title': 'Hearts Blood: The Pit Dragon Trilogy, Volume Two', 'rating': 5.0},
        {'title': 'A Writers Britain: Landscape in Literature', 'rating': 4.6},
        {'title': 'The Sound of a Miracle', 'rating': 4.8},
    ]
    evaluateSentiments(user_profile_books)

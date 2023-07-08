from functools import reduce

import dask.dataframe as ddf
from matplotlib import pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.graph_objects as go

"""
books_data.csv
"""


def get_books_data_df(file_name):
    training_data_ddf = ddf.read_csv(file_name, dtype={'Id': 'object'})
    rows_len = training_data_ddf.map_partitions(len).compute()
    total = reduce(lambda x, y: x + y, rows_len)
    print(total)
    return training_data_ddf


def exploreCategories(df):
    print("\nEntered function exploreCategories\n")

    # drop row which have no category
    enhanced_df = df.dropna(subset=['categories'])

    # As there are many genres, let's only work with only with those having over 2000 occurrences
    print("Value Counts: ", enhanced_df['categories'].value_counts().loc[lambda x: x >= 2000].compute())
    print("***************")
    print("Value Counts: ", enhanced_df['categories'].value_counts().compute())

    plt.figure(figsize=(10, 12))
    sns.barplot(x=enhanced_df['categories'].value_counts().loc[lambda x: x >= 2000].compute().index,
                y=enhanced_df['categories'].value_counts().loc[lambda x: x >= 2000].compute())

    plt.xticks(rotation=30, ha='right')
    plt.title("Genre count")
    plt.xlabel("Genres")
    plt.ylabel("Count")
    plt.show()

    # Generating a pie chart for target label 'categories'
    plt.figure(figsize=(10, 8))
    plt.pie(x=enhanced_df['categories'].value_counts().loc[lambda x: x >= 2000].compute(),
            labels=enhanced_df['categories'].value_counts().loc[lambda x: x >= 2000].compute().index,
            textprops={'fontsize': 10}, startangle=150, autopct='%1.0f%%')
    plt.title('Genre Count')
    plt.show()


# most predominant genres

def freqReviews(books_df):
    """
    Most frequent words in 4+ star reviews
    :param books_df:
    :return:
    """
    wc = WordCloud(width=500, height=500, min_font_size=15, background_color='black')

    initial_text = books_df[(books_df['score'] >= 0) & (books_df['score'] < 2)]['reviewtext'].compute().head(50000)

    print(initial_text)
    all_text = initial_text.str.cat(sep=" ")
    f = open("reviews_big.txt", "a")
    f.write(all_text)
    f.close()

    spam_wc = wc.generate(all_text)

    plt.figure(figsize=(20, 10))
    plt.axis('off')
    plt.imshow(spam_wc)
    plt.axis('off')
    plt.show()


def review_distribution(books_df):
    colors = ['gold', 'mediumturquoise', 'brown']
    labels = books_df['score'].value_counts().compute().keys().map(str)
    print(labels)
    values = books_df['score'].value_counts() / books_df['score'].value_counts().shape[0]
    print(values.compute())

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_traces(hoverinfo='label+percent', textinfo='percent', textfont_size=20,
                      marker=dict(colors=colors, line=dict(color='white', width=0.1)))

    fig.show()


def author_book_count(book_df):
    print(book_df['authors'].value_counts().head(20).sort_values(ascending=True))
    book_df['authors'].value_counts().head(20).sort_values(ascending=True).plot(kind='barh', figsize=(15, 10))
    plt.title('Number of Books written by the Authors', fontsize=15)
    plt.grid(visible=True, which='both')
    plt.show()


def test_book_data():
    books_df = get_books_data_df("../books_data.csv")
    books_df = books_df.dropna(subset=['description', 'Title', 'categories'])
    # exploreCategories(books_df)
    author_book_count(books_df)


def test_book_ratings():
    ratings_df = get_books_data_df("ratings.csv")
    # freqReviews(ratings_df)
    review_distribution(ratings_df)


test_book_data()

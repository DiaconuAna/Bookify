import time
import pandas as pd

from datasets.review_sentiment_analysis.review_analysis import analyseText

'''
Extracting keywords from book descriptions and user reviews
'''
from datasets.recommendations.keyword_recommender import yake_pke


def extractDescriptionKeywords(books_df):
    f = open("book_descr_keywords_2.txt", "a", encoding="utf-8")

    for x, row in books_df.iterrows():
        start = time.time()
        print(x, row['Title'])
        if x >= 0:
            description = row['description']
            keywords_descr = yake_pke(description)
            authors = row['authors']
            if isinstance(authors, str):
                authors = authors[2:-2].split(",")
                for author in authors:
                    print(author)
                    keywords_descr.append(author.lower())
            categories = row['categories'][2:-2]
            categories = categories.lower()
            if categories not in keywords_descr:
                keywords_descr.append(categories)
            print(keywords_descr)
            f.write(row['Title'] + "\n")
            f.write(str(keywords_descr))
            f.write("\n")
        end = time.time()
        print("Time spent: " + str(end - start))

    f.close()


'''
Convert the keyword-title file to a pandas dataframe
'''


def description_to_pandas(filename="book_descr_keywords_2.txt"):
    keyword_dict = {}
    descr_file = open(filename, 'r', encoding='latin-1')

    while True:
        title = descr_file.readline()
        if not title:
            break
        keyword_list_str = descr_file.readline()
        if not keyword_list_str:
            break
        keyword_list_str = keyword_list_str[1:-2]
        keyword_list_str = keyword_list_str.replace("\'", "")
        keyword_list_tmp = keyword_list_str.split(",")
        keyword_list = []
        for k in keyword_list_tmp:
            if k[0] == ' ':
                keyword_list.append(k[1:])
            else:
                keyword_list.append(k)
        keyword_dict[title] = keyword_list

    keywords = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in keyword_dict.items()])).transpose()
    keywords = keywords.apply(lambda x: ','.join(x.dropna()), axis=1)
    keywords = pd.DataFrame(keywords)
    keywords.rename(columns={-1: 'title', 0: 'keywords'}, inplace=True)  # todo - figure out how to create 2 columns
    # Save the plots to a CSV
    keywords.to_csv(path_or_buf='Descr_keywords_2.csv')
    print('saved')


'''
Miscellaneous
'''


def processPandasDataframe(filename='Book-keywords.csv'):
    keywords = pd.read_csv(filename)
    # keywords.rename(columns={'Unnamed: 0': 'tconst'}, inplace=True)
    # keywords.set_index('tconst', inplace = True)
    print(len(keywords))
    # print("Columns")
    # print(keywords.columns)
    # print('******')
    # print(keywords.head(10))
    # print('******')
    # print(keywords['keywords'])
    # print('******')
    # print(keywords['title'])

    return keywords


'''
Building the book emotions dataset
'''


def extractSentiment(concept_words, books_df):
    f = open("book_emotions.txt", "a", encoding="utf-8")

    for x, row in books_df.iterrows():
        start = time.time()
        print(x, row['Title'])
        if x >= 0:
            description = row['description']
            sentiments = analyseText(concept_words, description)
            polarity = sentiments.pop('polarity', None)
            scores = sorted(sentiments.items(), key=lambda x: x[1], reverse=True)[:5]
            top_sentiments = [x[0] for x in scores]
            print(top_sentiments)
            f.write(row['Title'] + "\n")
            f.write(str(top_sentiments) + "\n")
            f.write(str(polarity))
            f.write("\n")
        end = time.time()
        print("Time spent: " + str(end - start))

    f.close()


def analyseTextToPandas(filename="book_emotions.txt"):
    sentiment_dict = []
    descr_file = open(filename, 'r', encoding='latin-1')

    while True:
        title = descr_file.readline()
        if not title:
            break
        sentiments = descr_file.readline()
        if not sentiments:
            break
        polarity = descr_file.readline()
        if not polarity:
            break
        sentiments = sentiments[1:-2]
        sentiments = sentiments.replace("\'", "")
        sentiments = sentiments.split(",")
        sentiment_list = []
        for s in sentiments:
            if s[0] == ' ':
                sentiment_list.append(s[1:])
            else:
                sentiment_list.append(s)

        element = {'title': title, 'sentiments': sentiment_list, 'polarity': polarity}
        sentiment_dict.append(element)

    sentiment_df = pd.DataFrame(sentiment_dict)
    sentiment_df.to_csv(path_or_buf="book_emotions.csv")

    print('saved')

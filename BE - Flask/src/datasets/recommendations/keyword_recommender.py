import pandas as pd

import dask.dataframe as ddf
from dask.diagnostics import ProgressBar
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import pandas as pd

from gensim.corpora.dictionary import Dictionary
from gensim.models.tfidfmodel import TfidfModel
from gensim.similarities import MatrixSimilarity

from pke.unsupervised import YAKE

"""
Description keywords dataset
"""


def processDescriptionDataset():
    books_df = ddf.read_csv("src\\datasets\\Description_keywords.csv",
                            dtype={'Id': 'object'})
    # books_df = ddf.read_csv("src\\datasets\\Description_keywords.csv", dtype={'Id': 'object'})
    books_df['title'] = books_df['title'].replace('\n\r', '', regex=True)

    return books_df


"""
keyword extraction
"""


def text_to_keywords(text):
    if len(text) > 1000000:
        text = text[:1000000]
    return yake_pke(text)


def yake_pke(text='', stop_words=['book']):
    # 1. Create YAKE keyword extractor
    extractor = YAKE()

    # 2. Load document
    # extractor.load_document(input=text, language='en', normalization=None)

    stoplist = stopwords.words('english')
    stoplist.extend(stop_words)
    extractor.load_document(input=text,
                            language='en',
                            stoplist=stoplist,
                            normalization=None)

    # 3. Generate candidate 1-gram, 2-gram and 3-gram keywords
    extractor.candidate_selection(n=1)

    # 4. Calculate scores for the candidate keywords
    extractor.candidate_weighting(window=2, use_stems=False)

    # 5. Select 10 highest ranked keywords
    # Remove redundant keywords with similarity above 80%
    key_phrases = extractor.get_n_best(n=15, threshold=0.8)
    result = []
    for k in key_phrases:
        result.append(k[0])

    return result


"""
auxiliary functions
"""


def remove_commas(text):
    no_commas = [t for t in text if t != ',']
    return no_commas


"""
recommender systems
"""


def model1_tf_idf(book_df, user_keywords, n):
    book_df.reset_index(inplace=True)

    keywords = book_df['keywords'].tolist()
    keywords = [keyword.lower().split(',') for keyword in keywords]
    # print(keywords)
    processed_keywords = [remove_commas(keyword) for keyword in keywords]
    # print(processed_keywords)

    # create word dictionary using gensim
    dictionary = Dictionary(processed_keywords)
    # create corpus where the corpus is a bag of words for each document
    corpus = [dictionary.doc2bow(doc) for doc in processed_keywords]
    tfidf = TfidfModel(corpus)  # create tfidf model of the corpus

    # Create the similarity data structure. This is the most important part where we get the similarities between the
    # books.
    sims = MatrixSimilarity(tfidf[corpus], num_features=len(dictionary))

    query_doc_bow = dictionary.doc2bow(user_keywords)  # get a bag of words from the query_doc
    # print(query_doc_bow)
    query_doc_tfidf = tfidf[query_doc_bow]  # convert the regular bag of words model to a tf-idf model where we have
    # tuples of the book title and its tf-idf value for the book
    similarity_array = sims[query_doc_tfidf]
    similarity_series = pd.Series(similarity_array.tolist(), index=book_df.title.values)  # Convert to a Series
    top_hits = similarity_series.sort_values(ascending=False)[:n]  # get the top matching results,
    # i.e. most similar books

    results = []
    for idx, (book, score) in enumerate(zip(top_hits.index, top_hits)):
        # print("%d '%s' with a similarity score of %.3f" % (idx + 1, book, score))
        results.append((book, score))

    return results


def model2_cosine(book_df, user_keywords, n):
    new_row = book_df.iloc[-1, :].copy()  # copy of the last row used for user's input

    row_structure = (str(user_keywords).replace('\'', '').replace(' ', ''))[
                    1:-1]  # {"title": "", "keywords": user_keywords}
    new_row.iloc[-1] = row_structure  # add user input to the row

    book_df = book_df.append(new_row, ignore_index=True)

    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(book_df.keywords.tolist())

    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

    sim_scores = list(enumerate(cosine_sim2[-1, :]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    ranked_titles = []

    for i in range(1, n + 1):
        indx = sim_scores[i][0]
        ranked_titles.append((book_df['title'].iloc[indx], sim_scores[i][1]))

    return ranked_titles


def description_recommender(keyword_list, top_rec=10):
    model1 = []
    with pd.read_csv('src\\datasets\\Description_keywords.csv',
                     chunksize=5000) as reader:
        for chunk in reader:
            model1.extend(model2_cosine(chunk, keyword_list, 10))
    sorted_recs = sorted(model1, key=lambda x: x[1], reverse=True)
    return sorted_recs[:top_rec]


"""
Evaluation: precision and recall
"""


def get_ground_truth(book_df, user_keywords):
    result = []
    for index, row in book_df.iterrows():
        keywords = row['keywords'].split(',')
        res, tr = similar_keywords(keywords, user_keywords, 0.2)
        if res:
            result.append(row['title'])
            print(row['title'])
    return result


def similar_keywords(book_keywords, user_keywords, threshold=0.2):
    # Combine the keywords into two strings
    keywords_str_1 = ' '.join(book_keywords)
    keywords_str_2 = ' '.join(user_keywords)

    # Vectorize the keywords using CountVectorizer
    vectorizer = CountVectorizer().fit_transform([keywords_str_1, keywords_str_2])

    # Compute the cosine similarity between the two sets of keywords
    cosine_sim = cosine_similarity(vectorizer)[0][1]

    if cosine_sim >= threshold:
        print("Book is similar to user's keywords.", threshold)
        return True, cosine_sim
    else:
        # print("Book is dissimilar to user's keywords.")
        return False, cosine_sim


def isInGT(title, gt):
    return title in gt


def evaluateKeywordModel1(books_df, user_keywords, ground_truth=[]):
    tp = 0  # recommended book in gt
    fp = 0  # recommended book not in gt

    recommended_books = description_recommender(user_keywords, 15)

    for row in recommended_books:
        keywords = books_df.loc[books_df['title'] == row[0], 'keywords'].str.cat(sep=', ').compute().split(',')
        print(row[0])
        print(similar_keywords(keywords, user_keywords))
        if row[0] in ground_truth:
            print(row[0], "YES")
            tp = tp + 1
        else:
            fp = fp + 1
    fn = len(ground_truth) - tp

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    F1 = 2 * (precision * recall) / (precision + recall)

    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1: ", F1)


if __name__ == "__main__":
    books_df = processDescriptionDataset()
    # user_keywords = ['fairytale', 'fairy', 'dragon', 'story', 'garden', 'fantasy', 'magic', 'adventure', 'epic']
    # user_keywords = ['mystery', 'adventure', 'fantasy', 'romance', 'horror', 'suspense', 'action', 'thriller', 'detective', 'comedy', 'drama', 'western', 'sci-fi', 'time travel', 'historical fiction', 'paranormal', 'espionage', 'military', 'crime', 'spy', 'magic', 'supernatural', 'mythology', 'aliens', 'robots', 'space opera', 'post-apocalyptic', 'dystopian', 'vampires', 'zombies']
    # user_keywords = ['happy', 'sad', 'big', 'small', 'funny', 'serious', 'good', 'bad', 'young', 'old', 'beautiful', 'ugly', 'tall', 'short', 'long', 'wide', 'narrow', 'fast', 'slow', 'hot', 'cold', 'bright', 'dark', 'loud', 'quiet', 'hard', 'soft', 'heavy', 'light', 'thick']
    # user_keywords = ['happy', 'sad', 'big', 'small', 'funny', 'serious', 'good', 'bad', 'young', 'old', 'beautiful', 'ugly', 'tall', 'light', 'thick', 'sometimes','funny', 'ultimately', 'sad', 'hiding', 'behind', 'closed', 'doors', 'comment', 'four', 'beautiful', 'young']

    # user_keywords = ["monsters", "fighting", "adventures", "betrayal", "creatures", "myths", "legends", "survival", "heroes", "challenges"]
    # user_keywords = ["biography", "leader", "influence", "legacy", "achievements", "challenges", "visionary", "inspiration", "motivation", "adversity"]
    # user_keywords = ['faith', 'spirituality', 'religion', 'belief', 'prayer', 'meditation', 'enlightenment', 'divine', 'worship', 'soul', 'healing', 'god', 'sacred', 'peace', 'transcendence']
    # user_keywords = ["computer science", "programming", "data structures", "algorithms", "machine learning", "artificial intelligence", "natural language processing", "deep learning", "neural networks", "computer vision", "big data", "data mining", "database systems", "web development", "networking"]
    # user_keywords = ['children', 'fiction', 'fantasy', 'adventure', 'magic', 'mystery', 'humor', 'animals', 'school', 'friendship']
    # user_keywords = ['history', 'historical', 'biography', 'war', 'politics', 'culture', 'society', 'civilization', 'revolution', 'colonial']
    # user_keywords = ['love', 'romance', 'passion', 'heartbreak', 'relationship', 'affair', 'intimacy', 'seduction', 'commitment', 'desire']
    # user_keywords = ['travel', 'adventure', 'exploration', 'journey', 'culture', 'discovery', 'expedition', 'tourism', 'voyage', 'wanderlust']
    # user_keywords = ['art', 'design', 'creativity', 'aesthetics', 'visual', 'graphic', 'illustration', 'painting', 'sculpture', 'architecture']
    # user_keywords = ['sports', 'athletics', 'fitness', 'exercise', 'competition', 'teamwork', 'strategy', 'training', 'champion', 'victory']
    user_keywords = ['self-help', 'motivation', 'self-improvement', 'positive', 'mindset', 'growth', 'success',
                     'confidence', 'happiness', 'empowerment']
    gt = get_ground_truth(books_df, user_keywords)
    evaluateKeywordModel1(books_df, user_keywords, gt)

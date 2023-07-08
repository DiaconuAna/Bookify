import csv


def formConcepts():
    concept_words = {}
    with open('src\\datasets\\senticnet\\senticnet.csv', 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:

            concept_words[row[0]] = {
                'emotion': row[5][1:],
                'polarity': row[8]
            }
    return concept_words


def analyseText(concept_words, text):
    sentiment_scores = {'grief': 0, 'anxiety': 0, 'annoyance': 0, 'contentment': 0, 'melancholy': 0,
                        'enthusiasm': 0, 'ecstasy': 0, 'bliss': 0, 'loathing': 0, 'dislike': 0, 'acceptance': 0,
                        'calmness': 0, 'fear': 0, 'responsiveness': 0, 'pleasantness': 0, 'terror': 0, 'disgust': 0,
                        'eagerness': 0, 'rage': 0, 'serenity': 0, 'joy': 0, 'anger': 0, 'sadness': 0, 'delight': 0}
    polarity = 0
    polarity_count = 0
    for word in text.split():
        if word in concept_words.keys() and concept_words[word]['emotion'] in sentiment_scores.keys():
            sentiment_scores[concept_words[word]['emotion']] += 1
            polarity += float(concept_words[word]['polarity'])
            polarity_count += 1

    sentiment_scores = sorted(sentiment_scores.items(), key = lambda x:x[1], reverse=True)[:5]
    sentiment_labels = [x[0] for x in sentiment_scores]
    return sentiment_labels, polarity/polarity_count

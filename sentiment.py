from textblob import TextBlob


def sentiment(text):
    blob = TextBlob(text)
    print(blob)
    senti = blob.sentiment.polarity
    return round(senti, 2)


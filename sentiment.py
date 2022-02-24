from textblob import TextBlob


def sentiment(text):
    text = f"{text}"
    blob = TextBlob(text)
    senti = blob.sentiment.polarity
    return round(senti, 2)


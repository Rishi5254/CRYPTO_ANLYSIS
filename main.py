from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import newapi
import gnews
import content_extract
import sentiment

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CONFIGURE TABLES

class Articles(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    content = db.Column(db.String())
    date = db.Column(db.String(10))
    url = db.Column(db.String(), unique=True)
    img_url = db.Column(db.String())
    article_source = db.Column(db.String())
    topic_related = db.Column(db.String())
    main_source = db.Column(db.String())
    title_sentiment = db.Column(db.Integer)
    description_sentiment = db.Column(db.Integer)
    content_sentiment = db.Column(db.Integer)
    overall_sentiment = db.Column(db.Integer)


db.create_all()


def add_to_db(title, description, content, date, url, img_url, article_source, topic_related,
              main_source, title_sentiment, description_sentiment, content_sentiment, overall_sentiment):
    content = content.replace("\n", "")
    content = content.replace("  ", "")
    content = content.replace("\t", "")
    try:
        new_article = Articles(title=title, description=description, content=content, date=date, url=url, img_url=img_url,
                               article_source=article_source, topic_related=topic_related, main_source=main_source,
                               title_sentiment=title_sentiment, description_sentiment=description_sentiment,
                               content_sentiment=content_sentiment, overall_sentiment=overall_sentiment)

        db.session.add(new_article)
        db.session.commit()
        print(date, title, topic_related )
    except exc.IntegrityError:
        db.session.rollback()
        print("rolled back...... ")
        article = db.session.query(Articles).filter_by(url=url).first()
        topic = article.topic_related
        topics = topic.split(",")
        if topic_related not in topics:
            article.topic_related = f"{topic},{topic_related}"
            db.session.commit()
            print("comma added.......")


queries = ["bitcoin", "ethereum", "dogecoin", "litecoin", "ripple", "tether coin", "Binance coin", "ntf"]


def data_extract(date, query):
    date = date.split("-")
    day = date[0]
    month = date[1]
    year = date[2]

    newapi_data = newapi.extract_data(day, month, year, query, False)

    for data in newapi_data:
        title = data.get("title")
        description = data.get("description")
        content = content_extract.content_extractor(data.get("url"))
        if len(content) < 25:
            content = data.get('content')
        date = data.get("publishedAt").split("T")[0]
        url = data.get("url")
        img_url = data.get("urlToImage")
        article_source = data.get("source").get("name")
        topic_related = query
        main_source = "newapi.org"
        title_sentiment = sentiment.sentiment(title)
        description_sentient = sentiment.sentiment(description)
        content_sentiment = sentiment.sentiment(content)
        overall_sentiment = title_sentiment + description_sentient + content_sentiment

        add_to_db(title, description, content, date, url, img_url, article_source, topic_related, main_source,
                  title_sentiment, description_sentient, content_sentiment, overall_sentiment )

    gnews_data = gnews.extract_data(day, month, year, query)

    for data in gnews_data:
        title = data.get("title")
        description = data.get("description")
        content = data.get("content")
        date = data.get("publishedAt").split("T")[0]
        url = data.get("url")
        img_url = data.get("image")
        article_source = data.get("source").get("name")
        topic_related = query
        main_source = "gnews_api"
        title_sentiment = sentiment.sentiment(title)
        description_sentient = sentiment.sentiment(description)
        content_sentiment = sentiment.sentiment(content)
        overall_sentiment = title_sentiment + description_sentient + content_sentiment

        add_to_db(title, description, content, date, url, img_url, article_source, topic_related, main_source,
                  title_sentiment, description_sentient, content_sentiment, overall_sentiment)



#
# if __name__ == "__main__":d
#     app.run(debug=True)
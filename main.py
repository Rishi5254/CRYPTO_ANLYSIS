from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

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
    try:
        new_article = Articles(title=title, description=description, content=content, date=date, url=url, img_url=img_url,
                               article_source=article_source, topic_related=topic_related, main_source=main_source,
                               title_sentiment=title_sentiment, description_sentiment=description_sentiment,
                               content_sentiment=content_sentiment, overall_sentiment=overall_sentiment)

        db.session.add(new_article)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        article = db.session.query(Articles).filter_by(url=url).first()
        topic = article.topic_related
        topics = topic.split(",")
        if topic_related not in topics:
            article.topic_related = f"{topic},{topic_related}"
            db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)
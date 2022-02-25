from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_bootstrap import Bootstrap
import newapi
import gnews
import content_extract
import sentiment
import forms
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

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


def data_extract(date, query):
    date = date.split("-")
    day = date[0]
    month = date[1]
    year = date[2]
    print(day, month, year)
    newapi_data = newapi.extract_data(day, month, year, query, False)

    for data in newapi_data:

        title = data.get("title")
        description = data.get("description")
        content = content_extract.content_extractor(data.get("url"))
        if len(content) < 50:
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
        overall_sentiment = round(title_sentiment + description_sentient + content_sentiment, 2)

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


queries = ["bitcoin", "ethereum", "dogecoin", "litecoin", "ripple", "tether coin", "Binance coin", "nft"]
#
# for i in range(7, 8):
#     data_extract("25-1-2022", queries[i])


@app.route('/', methods=['GET', 'POST'])
def homepage():
    dict = {}
    final_dict = {'normal': [],
                  'positive': [],
                  'negative': []
                  }
    date = datetime.datetime.now().date()
    date = "2022-01-19"
    for coin in queries:
        data = Articles.query.filter(Articles.topic_related.contains(coin), Articles.date == date).all()
        for index, article in enumerate(data):
            if index == 0:
                dict[coin] = []
                dict[coin].append(article.title_sentiment)
            else:
                dict[coin].append(article.title_sentiment)
    for query in dict:
        values = dict[query]
        for value in values:
            if value == 0:
                final_dict['normal'].append(value)
            elif value > 0:
                final_dict['positive'].append(value)
            else:
                final_dict['negative'].append(value)
        dict[query] = final_dict
        final_dict = {'normal': [],
                      'positive': [],
                      'negative': []
                      }

    print(dict)


    return render_template('index.html', data=dict)


@app.route('/table')
def table():
    form = forms.DataPicker()
    if form.validate_on_submit():
        date = form.date.data
        data = Articles.query.filter(Articles.topic_related.contains(query), Articles.date == date).all()
        return render_template('index.html', data=data, form=form)
    return render_template('table.html', form)


if __name__ == "__main__":
    app.run(debug=True)
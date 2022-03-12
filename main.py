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
import cryptoprices
import dateoutput

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


class Prices(db.Model):
    __tablename__ = "prices"
    id = db.Column(db.Integer, primary_key=True)
    coin_name = db.Column(db.String())
    coin_code = db.Column(db.String())
    date = db.Column(db.String(10))
    open = db.Column(db.String())
    high = db.Column(db.String())
    low = db.Column(db.String())
    close = db.Column(db.String())
    adj_close = db.Column(db.String())
    Volume = db.Column(db.String())


db.create_all()

queries = ["bitcoin", "ethereum", "dogecoin", "litecoin", "tether coin", "Binance coin", "nft"]


def crypto_prices():
    for i in queries[0:6]:
        data, code = cryptoprices.content_extractor(i)
        for date in data:
            check_price = Prices.query.filter(Prices.coin_code.contains(code),
                                              Prices.date == date).first()
            if check_price != None:
                update_price = Prices.query.get(check_price.id)
                update_price.open = data[date][0]
                update_price.high = data[date][1]
                update_price.low = data[date][2]
                update_price.close = data[date][3]
                update_price.adj_close = data[date][4]
                update_price.Volume = data[date][5]
                db.session.commit()
            else:
                price = Prices(coin_name=i, coin_code=code, date=date, open=data[date][0], high=data[date][1], low=data[date][2], close=data[date][3], adj_close=data[date][4], Volume=data[date][5])
                db.session.add(price)
                db.session.commit()

# try:
#     crypto_prices()
# except:
#     print("failed updating crypto prices")


def candlesticks(date, query):
    details = []

    present_data = Prices.query.filter(Prices.coin_name.contains(query), Prices.date == date).first()
    if present_data is not None:
        details.append([present_data.date, float(str(present_data.open).replace(",", "")),
                        float(str(present_data.high).replace(",", "")), float(str(present_data.low).replace(",", "")),
                        float(str(present_data.close).replace(",", ""))])
    else:
        not_got = True
        print(date)
        present_date = date
        while not_got:
            previous_date = dateoutput.date_sequence(present_date, "p")
            print(previous_date)
            past_data = Prices.query.filter(Prices.coin_name.contains(query), Prices.date == previous_date).first()
            if past_data is not None:
                details.append([past_data.date, float(str(past_data.open).replace(",", "")),
                                float(str(past_data.high).replace(",", "")), float(str(past_data.low).replace(",", "")),
                                float(str(past_data.close).replace(",", ""))])
                not_got = False
            else:
                print("hi")
                present_date = previous_date

    print(details)
    for i in range(1, 3):
        if i == 1:
            i = "n"
        else:
            i = "p"
        not_got_past = True
        present_date = date
        while not_got_past:
            previous_date = dateoutput.date_sequence(present_date, i)
            print(f"previous ra : {previous_date}")
            print(previous_date)
            past_data = Prices.query.filter(Prices.coin_name.contains(query), Prices.date == previous_date).first()
            if past_data is not None:
                details.append([past_data.date, float(str(past_data.open).replace(",", "")),
                                float(str(past_data.high).replace(",", "")), float(str(past_data.low).replace(",", "")),
                                float(str(past_data.close).replace(",", ""))])
                not_got_past = False
            else:
                print("hi")
                present_date = previous_date

    return details


def add_to_db(title, description, content, date, url, img_url, article_source, topic_related,
              main_source, title_sentiment, description_sentiment, content_sentiment, overall_sentiment):
    content = content.replace("  ", "")
    content = content.replace("\t", "")
    try:
        new_article = Articles(title=title, description=description, content=content, date=date, url=url,
                               img_url=img_url,
                               article_source=article_source, topic_related=topic_related, main_source=main_source,
                               title_sentiment=title_sentiment, description_sentiment=description_sentiment,
                               content_sentiment=content_sentiment, overall_sentiment=overall_sentiment)

        db.session.add(new_article)
        db.session.commit()
        print(date, title, topic_related)
    except exc.IntegrityError:
        try:
            db.session.rollback()
            print("rolled back...... ")
            article = db.session.query(Articles).filter_by(url=url).first()
            topic = article.topic_related
            topics = topic.split(",")
            if topic_related not in topics:
                article.topic_related = f"{topic},{topic_related}"
                db.session.commit()
                print("comma added.......")
        except:
            db.session.rollback()
            print("ROLLED BACK FOR GOOD")


def data_extract(date, query):
    date = date.split("-")
    day = date[0]
    month = date[1]
    year = date[2]
    print(day, month, year)
    newapi_data = newapi.extract_data(day, month, year, query, True)

    for data in newapi_data:
        present = False
        content = ""
        url = data.get("url")
        article = db.session.query(Articles).filter_by(url=url).first()
        if article:
            present = True
            content = article.content

        title = data.get("title")
        description = data.get("description")
        if not present:
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
                  title_sentiment, description_sentient, content_sentiment, overall_sentiment)

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


# for i in range(7, 10):
#     for query in queries:
#         data_extract(f"{i}-03-2022", query)


@app.route('/', methods=['GET', 'POST'])
def homepage():
    form = forms.Update()
    candle = [['2022-02-24', 9.5425, 9.5447, 8.2483, 9.3365], ['2022-02-25', 9.3388, 9.6207, 9.1207, 9.5752],
              ['2022-02-26', 9.5747, 9.7625, 9.4719, 9.5831]]
    dict = {}
    final_dict = {'normal': [],
                  'positive': [],
                  'negative': []
                  }
    date = datetime.datetime.now().date()
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
                      'negative': [],
                      }
    for query in dict:
        values = dict[query]
        for value in values:
            dict[query][value] = len(values[value])
    if form.validate_on_submit():
        date = str(date)
        date = date.split("-")
        date = f"{date[2]}-{date[1]}-{date[0]}"
        for query in queries:
            print(date, query)
            data_extract(date, query)
        return redirect(url_for("homepage"))
    return render_template('index.html', data=dict, candle=candle, form=form)


@app.route('/table', methods=['GET', 'POST'])
def table():
    form = forms.DataPicker()
    if form.validate_on_submit():
        final_dict = {'normal': [],
                      'positive': [],
                      'negative': []
                      }
        query = form.query.data
        date = form.date.data
        print(f"cadle data = {date}")
        candel = candlesticks(date, query)

        data = Articles.query.filter(Articles.topic_related.contains(query), Articles.date == date).all()
        for article in data:
            if article.title_sentiment == 0:
                final_dict['normal'].append(article.title_sentiment)
            elif article.title_sentiment > 0:
                final_dict['positive'].append(article.title_sentiment)
            else:
                final_dict['negative'].append(article.title_sentiment)
        for sentiment in final_dict:
            final_dict[sentiment] = len(final_dict[sentiment])

        return render_template('table.html', articles=data, form=form, senti=final_dict, query=query, candle=candel)
    return render_template('table.html', form=form)


@app.route('/article/<int:id>', methods=['GET', 'POST'])
def article_details(id):
    article = Articles.query.get(id)
    return render_template('article.html', article=article)


@app.route("/trial")
def trial():
    return render_template("trial.html")

# print(candlesticks("2022-02-31", "bitcoin"))


if __name__ == "__main__":
    app.run(debug=True)

from datetime import datetime, timedelta
import time
import urllib.request
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

symbols = {"bitcoin": 'BTC',
           "ethereum": 'ETH',
           "dogecoin": 'DOGE',
           "litecoin": 'LTC',
           "tether coin": 'USDT',
           "Binance coin": 'BNB',
           }
months = {'Jan': '01',
          'Feb': '02',
          'Mar': '03',
          'Apr': '04',
          'May': '05',
          'Jun': '06',
          'Jul': '07',
          'Aug': '08',
          'Sept': '09',
          'Oct': '10',
          'Nov': '11',
          'Dec': '12',
          }


# WEB SCRAPING
def extracter(url):

    req = Request(url, headers={'User-Agent': 'XYZ/3.0'})
    webpage = urlopen(req, timeout=10).read()
    webpage = webpage.decode('utf-8')
    soup = BeautifulSoup(webpage, "lxml")

    all_data = {}

    for para in soup.find_all("td"):
        data = para.get_text().split(" ")
        if len(data) == 3 or len(data) == 1:
            if len(data) == 3:
                if data[1] in months:
                    data[1] = months[data[1]]
                date = f"{data[2]}-{data[1]}-{data[0]}"
                all_data[date] = []
            else:
                last_key = list(all_data.keys())[-1]
                all_data[last_key].append(data[0])
    return all_data


def content_extractor(coin_name):
    dtime = datetime.now() + timedelta(seconds=3)
    unixtime = round(time.mktime(dtime.timetuple()) - 30)
    url = f"https://sg.finance.yahoo.com/quote/{symbols[coin_name]}-INR/history?period1={unixtime}&period2={unixtime}&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"
    try:
        content = extracter(url)
        return content, symbols[coin_name]
    except urllib.error.HTTPError as err:
        try:
            content = extracter(url)
            return content, symbols[coin_name]
        except:
            return f"{err.code}"
    except urllib.error.URLError as err:
        return f"{err} : Invalid URL"
    except:
        return "Invalid url"

print(content_extractor("dogecoin"))
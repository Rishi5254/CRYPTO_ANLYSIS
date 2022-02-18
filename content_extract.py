import urllib.request
from urllib.error import HTTPError
from bs4 import BeautifulSoup


def content_extractor(url):
    try:
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, "lxml")

        data = ""
        for para in soup.find_all("p"):
            data += para.get_text()
            data += "\n"
        for para in soup.find_all("h2"):
            data += para.get_text()
            data += "\n"
        for para in soup.find_all("h2"):
            data += para.get_text()
            data += "\n"
        for para in soup.find_all("h2"):
            data += para.get_text()
            data += "\n"
        return data
    except urllib.error.HTTPError as err:
        return f"{err.code} : Invalid URL"

    except urllib.error.URLError as err:
        return f"{err} : Invalid URL"
    except:
        return "Invalid url"

print(content_extractor("https://economictimes.indiatimes.com/markets/cryptocurrency/top-cryptocurrency-prices-today-bitcoin-ethereum-slip-cardano-zooms-7/articleshow/88964726.cms"))

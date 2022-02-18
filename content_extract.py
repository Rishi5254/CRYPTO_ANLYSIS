import urllib.request
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup


def extracter(url):
    req = Request(url, headers={'User-Agent': 'XYZ/3.0'})
    webpage = urlopen(req, timeout=10).read()
    webpage = webpage.decode('utf-8')
    soup = BeautifulSoup(webpage, "lxml")
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


def content_extractor(url):
    url = f"{url}"
    try:
        content = extracter(url)
        return content

    except urllib.error.HTTPError as err:
        try:
            content = extracter(url)
            return content
        except:
            return f"{err.code}"

    except urllib.error.URLError as err:
        try:
            content = extracter(url)
            return content
        except:
            return f"{err} : Invalid URL"
    except:
        try:
            content = extracter(url)
            return content
        except:
            return "Invalid url"

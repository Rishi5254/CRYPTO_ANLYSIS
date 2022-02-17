import urllib.request
from urllib.error import HTTPError
from bs4 import BeautifulSoup


def content_extractor(url):
    if url:
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
    else:
        return "url not present"


content_extractor("https://www.fool.com/investing/2022/02/15/top-cryptos-by-market-cap-which-should-you-buy/")
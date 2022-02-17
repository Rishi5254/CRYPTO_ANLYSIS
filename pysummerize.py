from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
import urllib.request
import requests
from bs4 import BeautifulSoup

url = "https://www.fool.com/investing/2022/02/15/top-cryptos-by-market-cap-which-should-you-buy/"

# response = requests.get(url=url)

html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, "lxml")


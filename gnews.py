import requests
import math

url = "https://gnews.io/api/v4/search"
api_key = "32578a0d3220f126cb8e57d8d94b883a"


def end_page(day, month, year, query):
    parameters = {
        "token": api_key,
        "topic": "crypto currency",
        "q": query,
        "lang": "en",
        "max": 100,
        "page": 1,
        "from": f"{year}-{month}-{day}T01:00:00Z",
        "to": f"{year}-{month}-{day}T23:59:59Z",
        "expand": "content",
    }
    response = requests.get(url=url, params=parameters).json()['totalArticles']
    print(response)
    return math.ceil(response/25)


def extract_data(day, month, year, query):
    if len(f"{month}") == 1:
        month = f"0{month}"
    if len(f"{day}") == 1:
        day = f"0{day}"
    last_page = end_page(day, month, year, query)
    all_data = []
    for page in range(1, last_page+1):
        parameters = {
            "token": api_key,
            "q": query,
            "lang": "en",
            "max": 100,
            "page": page,
            "from": f"{year}-{month}-{day}T01:00:00Z",
            "to": f"{year}-{month}-{day}T23:59:59Z",
            "expand": "content",
        }
        response = requests.get(url=url, params=parameters).json()['articles']
        all_data += response
    return all_data



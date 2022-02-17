import requests

api_keys = ["6dbd4a994f78422aa92361f3f9414ef3", "9c4756ec043f430b92ab1b859e0992ab", "b80ef242bfc44227928ca60839c4df43"]


def find_api():
    api_key = None
    is_found = True
    while is_found:
        for i in api_keys:
            api = i
            parameters = {
                "apiKey": api,
                "q": "bitcoin"
            }
            response = requests.get(url=f"https://newsapi.org/v2/everything", params=parameters).json()["status"]
            if response == "error":
                continue
            elif response == "ok":
                api_key = api
                is_found = False
                break
    return api_key


def end_page(day, month, year, query):
    api_key = find_api()
    url = "https://newsapi.org/v2/everything?"
    parameters = {
        "q": f"{query}",
        "apiKey": f"{api_key}",
        "from": f"{year}-{month}-{day}",
        "to": f"{year}-{month}-{day}",
        "language": "en",
    }
    response = requests.get(url=url, params=parameters).json()['totalResults']
    if response > 80:
        return 6
    elif response > 60:
        return 5
    elif response > 40:
        return 4
    elif response > 20:
        return 3
    elif response < 20:
        return 2
    else:
        return 1


def extract_data(day, month, year, query, query_type):
    last_page = 6
    all_data = []
    api_key = find_api()
    if query_type:
        last_page = end_page(day, month, year, query)
        print(last_page)
    for page in range(1, last_page):
        for i in range(1, 3):
            print(f"page no : {page}")
            if i == 1:
                sort = "relevancy"
            else:
                sort = "popularity"
            print(f"{sort}")
            url = "https://newsapi.org/v2/everything?"
            parameters = {
                "q": f"{query}",
                "apiKey": f"{api_key}",
                "from": f"{year}-{month}-{day}",
                "to": f"{year}-{month}-{day}",
                "language": "en",
                "sortBy": sort,
                "page": f"{page}"
            }
            response = requests.get(url=url, params=parameters).json()['articles']
            all_data += response
    return all_data


print(extract_data(15, 2, 2022, "ethereum", True))
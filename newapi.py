import requests

api_keys = ["6dbd4a994f78422aa92361f3f9414ef3", "9c4756ec043f430b92ab1b859e0992ab", "b80ef242bfc44227928ca60839c4df43",
            "59bfc41fc748407face53db87dc25fe2", "a4ddfe25e48946ee86fc3f8eec2cd750", "630edae7cb0a45a2b9f30afa61d09931",
            "669bc010ed1f49c3a114007fd7170055", "5a622e92fe7c4e34ad23da1e9ca787b9", "ab4d5a8bc3fa421c97baf62cda2ee2c7",
            "0ddcae549f6946c8bb5dec69adb59304", "605a3e4580ea45e99adf7f0269dcc411", "75775fa980144f8ba01be1469058dfa6",
            "b80ef242bfc44227928ca60839c4df43", "ee7294810d22439fb1189e209753d136", "9e2bd0863ab146a3976f1e1fde68bd67",
            "f1a06b2c80024e718eded43c5c0f5f1e", "5e8136c37da046d88062e3006d329f8b", "627de97068f646f09f757b1f02b5ebba",
            ]


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
            print(all_data)
    return all_data




import requests

api_keys = ["6dbd4a994f78422aa92361f3f9414ef3", "9c4756ec043f430b92ab1b859e0992ab", "b80ef242bfc44227928ca60839c4df43",
            "59bfc41fc748407face53db87dc25fe2", "a4ddfe25e48946ee86fc3f8eec2cd750", "630edae7cb0a45a2b9f30afa61d09931",
            "669bc010ed1f49c3a114007fd7170055", "5a622e92fe7c4e34ad23da1e9ca787b9", "ab4d5a8bc3fa421c97baf62cda2ee2c7",
            "0ddcae549f6946c8bb5dec69adb59304", "605a3e4580ea45e99adf7f0269dcc411", "75775fa980144f8ba01be1469058dfa6",
            "b80ef242bfc44227928ca60839c4df43", "ee7294810d22439fb1189e209753d136", "9e2bd0863ab146a3976f1e1fde68bd67",
            "f1a06b2c80024e718eded43c5c0f5f1e", "5e8136c37da046d88062e3006d329f8b", "627de97068f646f09f757b1f02b5ebba",
            "2e1248f189514a1c98940de9fba7c3f8", "c35c88e1f6b9415caae44b525092377d", "69af8aa0a42f4054aca9b4e15dfe4430",
            "8c68bce17dfc409481794f7954d318a3", "b95666d140394c42a078f1560afe70b2", "cc0c7897227a4c209b63eefc60f1e18b"]


def find_api():
    api_key_index = None
    is_found = True
    while is_found:
        for index, i in enumerate(api_keys):
            api = i
            parameters = {
                "apiKey": api,
                "q": "bitcoin",
            }
            response = requests.get(url=f"https://newsapi.org/v2/everything", params=parameters).json()
            response = response["status"]
            if response == "ok":
                api_key_index = index
                is_found = False
                break
    print(f"NEW API : {api_key_index}")
    return api_key_index


def parameters(query, api_index, day, month, year, sort, page):
    parameters = {
        "q": f"{query}",
        "apiKey": f"{api_keys[api_index]}",
        "from": f"{year}-{month}-{day}",
        "to": f"{year}-{month}-{day}",
        "language": "en",
        "sortBy": sort,
        "page": f"{page}"
    }
    return parameters


def end_page(day, month, year, query, api):
    url = "https://newsapi.org/v2/everything?"
    api_index = api
    response = 0
    print("tried")
    is_found = True
    while is_found:
        api_response = requests.get(url=url, params=parameters(query, api_index, day, month, year, "relevancy", 1)).json()
        print(api_response)
        if api_response['status'] == "ok":
            response = api_response['totalResults']
            break
        else:
            api_index += 1

    print(f"END PAGE RESPONSE : {response}")
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
    api_key_index = find_api()
    last_page = 6
    all_data = []
    if query_type:
        last_page = end_page(day, month, year, query, api_key_index)
        print(f"last page : {last_page}")
    for page in range(1, last_page):
        for i in range(1, 3):
            print(f"Page nO : {page} -- Inside : {i}")
            print(f"API INDEX: {api_key_index}")
            if i == 1:
                sort = "relevancy"
            else:
                sort = "popularity"
            url = "https://newsapi.org/v2/everything?"

            is_found = True
            while is_found:
                response = requests.get(url=url, params=parameters(query, api_key_index, day, month, year, sort, page)).json()
                print(response)
                print("\n")
                if response['status'] == "ok":
                    response = response['articles']
                    all_data += response
                    break
                else:
                    api_key_index += 1

    return all_data





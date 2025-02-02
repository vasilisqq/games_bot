import requests

session = requests.Session()
base_url = "https://ru.wiktionary.org/w/api.php"
params = {
    "action":"query",
    "format":"json",
    "titles": "абаба" # здесь слово, которое ищем
}

for i in range(501):
    response = session.get(url=base_url, params=params)

    for k, v in response.json()["query"]["pages"].items():
        print(response.json()["query"]["pages"])
        if k != "-1":
            pageId = v["pageid"]
        else:
            print("Нет такого слова в этом словаре")
        pageId = None
print('AAAAAAAAAAAAAAAAAAA')
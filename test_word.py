import requests

session = requests.Session()
base_url = "https://ru.wiktionary.org/w/api.php"
params = {
    "action":"query",
    "format":"json",
    "titles": "пизда" # здесь слово, которое ищем
}

response = session.get(url=base_url, params=params)

print(response.json()["query"]["pages"])
for k, v in response.json()["query"]["pages"].items():
    if k != "-1":
        pageId = v["pageid"]
    else:
        print("Нет такого слова в этом словаре")
        pageId = None
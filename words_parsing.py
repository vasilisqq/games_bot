import requests
from bs4 import BeautifulSoup
import json

letters = "йцукенгшщзхфывапролджэячсмитбю"

all_words = []
for j in letters:
    for i in range(1,100):
        r = requests.get(f"https://bezbukv.ru/mask/{j}%2A%2A%2A%2A?page={i}")
        html = r.text
        bs = BeautifulSoup(html, 'lxml')
        a = bs.find_all('div', attrs={"class": "view"})
        b = 0
        for element in a:
            q = element.get_text()[5:].strip()
            print(len(q), q)
            if "-" not in q:
                all_words.append(q)
        if len(a) != 100:
            break
with open("words.json", "w", encoding="UTF-8") as f:
    json.dump(all_words, f, ensure_ascii=False)
    f.close()
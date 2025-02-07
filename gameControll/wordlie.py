import random
import requests
from db.DAO import DAO
from aiogram.fsm.state import State, StatesGroup

class Wordlie (StatesGroup):
    rooms = {}
    words: list[str] = []
    send_word = State()
    answer_word = State()
    async def create_alone_game(self, user_id: int|str, word=None):
        self.rooms.update({user_id: {"word": random.choice(self.words) if word is None else word,
                           "attempts": 1}})
    
    async def check_correct_word(self, user_answer:str, user_id, reit=True):
        answer =["🟥","🟥","🟥","🟥","🟥"]
        elses = []
        properties = self.rooms[user_id]
        print(properties["word"])
        w:list = list(properties["word"])
        for i in range(5):
            if user_answer[i] == w[0]:
                answer[i] = "🟩"
            else:
                elses.append(user_answer[i])    
            w = w[1:]
            # print("оставшиеся", elses)
        w:list = list(properties["word"])
        for i in range(5):
            if user_answer[i] != w[i] and user_answer[i] in w:
                if answer[i] not in ["🟧", "🟩"]:
                    answer[i] = "🟧"
        ans = "".join(a for a in answer)
        for i in range(5):
            if ans[i] != "🟩":
                properties["attempts"] += 1
                if properties["attempts"] < 6:
                    return ans, None
                else:
                    await DAO.wordlie_change_rait(user_id, -5)
                    return f"😢 Увы, ты не отгадал слово. 😞 \n\n🔤 Слово загаданное: [{properties["word"]}] \n\n🥇Твой рейтинг: 🏆 -5", True
        if reit:
            await DAO.wordlie_change_rait(user_id, 7-properties["attempts"])
            ans = ("🎉 Поздравляю! 🎉 Ты отгадал слово! 🥳\n" +
f"🔤 Слово загаданное: [{properties["word"]}]\n"+
f"🕵️‍♂️ Попыток было: 🤯 {properties["attempts"]}\n"+
f"🥇Твой рейтинг:🏆 +{7-properties["attempts"]}")
        else:
            ans = ("🎉 Поздравляю! 🎉 Ты отгадал слово! 🥳\n" +
f"🔤 Слово загаданное: [{properties["word"]}]\n"+
f"🕵️‍♂️ Попыток было: 🤯 {properties["attempts"]}\n")
        return ans, True

    async def check_word_for_russian(self, string: str) -> bool:
        return all(ord('А') <= ord(char) <= ord('я') for char in string)
    
    async def check_word_available(self, word:str) -> bool:
        session = requests.Session()
        base_url = "https://ru.wiktionary.org/w/api.php"
        params = {
            "action":"query",
            "format":"json",
            "titles": word # здесь слово, которое ищем
        }
        response = session.get(url=base_url, params=params)
        for k in response.json()["query"]["pages"].keys():
            if k == "-1":
                return False
        return True

    async def get_user_by_name(self, username:str):
        return await DAO.get_user_id_by_username(username)

        

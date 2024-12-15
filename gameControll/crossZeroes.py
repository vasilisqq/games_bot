from aiogram.types import InlineKeyboardMarkup
import random

class CrossZeroes:
    #room_id: int = 0
    symbols = "XO"
    private_rooms: dict = {}
    async def create__private_room(self, username: str, 
                                   keyboard: InlineKeyboardMarkup, 
                                   inline:str) -> None:
        players = [username, ""]
        first = random.choice(players)
        self.private_rooms.update({inline: {"players": [username, ""],
                                            "first_player": first,
                                            "move": first, 
                                            "keyboard": keyboard
                                            }})
    async def check_win(self, id:str) -> bool:
        field = self.private_rooms[id]["keyboard"].inline_keyboard
        for i in range(0,8):
            match i:
                case 0:
                    l = field[0][0].text + field[0][1].text + field[0][2].text
                case 1:
                    l = field[1][0].text + field[1][1].text + field[1][2].text
                case 2:
                    l = field[2][0].text + field[2][1].text + field[2][2].text
                case 3:
                    l = field[0][0].text + field[1][0].text + field[2][0].text
                case 4:
                    l = field[0][1].text + field[1][1].text + field[2][1].text
                case 5:
                    l = field[0][2].text + field[1][2].text + field[2][2].text
                case 6:
                    l = field[0][0].text + field[1][1].text + field[2][2].text
                case 7:
                    l = field[0][2].text + field[1][1].text + field[2][0].text
                case _:
                    l = None
            if ((l == "XXX") or (l == "OOO")):
                return True


            




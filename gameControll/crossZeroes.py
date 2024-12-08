from aiogram.types import InlineKeyboardMarkup
import random

class CrossZeroes:
    #room_id: int = 0
    symbols = "XO"
    private_rooms: dict = {}
    async def create__private_room(self, username: str, keyboard: InlineKeyboardMarkup, inline:str) -> None:
        players = [username, ""]
        first = random.choice(players)
        self.private_rooms.update({inline: {"players": [username, ""],
                                            "first_player": first,
                                            "move": first, 
                                            "keyboard": keyboard
                                            }})
        


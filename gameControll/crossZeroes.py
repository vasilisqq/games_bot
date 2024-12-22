from aiogram.types import InlineKeyboardMarkup
import random
from aiogram.types import InlineKeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class CrossZeroes:
    #room_id: int = 0
    symbols = "XO"
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    private_rooms: dict = {}
    async def create__private_room(self, username: str, 
                                   keyboard: InlineKeyboardMarkup, 
                                   inline:str,
                                   reload=False) -> None:
        players = self.private_rooms[inline]["players"] if reload else [username, ""]
        first = random.choice(players)
        scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
        self.private_rooms.update({inline: {"players": players,
                                            "first_player": first,
                                            "move": first, 
                                            "keyboard": keyboard,
                                            "scheduler":scheduler
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
                field = await self.edit_win_markup(
                    field,
                    i,l
                )
                print(self.private_rooms[id]["keyboard"].inline_keyboard)
                return True
            
    async def is_draw(self, id:str) -> bool:
        field = self.private_rooms[id]["keyboard"].inline_keyboard
        for i in range(0,9):
            if i in range (0,3):
                if field[0][i].text == " ":
                    return False
            elif i in range (3,6):
                if field[1][i-3].text == " ":
                    return False
            elif i in range (6,9):
                if field[2][i-6].text == " ":
                    return False
        return True 

    async def edit_win_markup(self, 
                              field:InlineKeyboardMarkup,
                              i:int,
                              l:str) -> InlineKeyboardMarkup:
        symbol = "❎" if l == "XXX" else "🟢"
        match i:
                case 0:
                    field[0][0].text = symbol
                    field[0][1].text = symbol
                    field[0][2].text = symbol
                case 1:
                    field[1][0].text = symbol
                    field[1][1].text = symbol
                    field[1][2].text= symbol
                case 2:
                    field[2][0].text = symbol
                    field[2][1].text = symbol
                    field[2][2].text= symbol
                case 3:
                    field[0][0].text = symbol
                    field[1][0].text = symbol
                    field[2][0].text= symbol
                case 4:
                    field[0][1].text = symbol
                    field[1][1].text = symbol
                    field[2][1].text= symbol
                case 5:
                    field[0][2].text = symbol
                    field[1][2].text = symbol
                    field[2][2].text= symbol
                case 6:
                    field[0][0].text = symbol
                    field[1][1].text = symbol
                    field[2][2].text= symbol
                case 7:
                    field[0][2].text = symbol
                    field[1][1].text = symbol
                    field[2][0].text= symbol
                case _:
                    pass
        for i in range(0,9):
            if i in range (0,3):
                field[0][i].callback_data = " "
            elif i in range (3,6):
                field[1][i-3].callback_data = " "
            elif i in range (6,9):
                field[2][i-6].callback_data = " "
        field.append([InlineKeyboardButton(text="заново", 
                                                 callback_data="reload_cross_zeroes_inline")])
        return field
    





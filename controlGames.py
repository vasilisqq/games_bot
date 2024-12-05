from aiogram import Router
from aiogram.types import Message
from commands import game

router_m = Router()

@router_m.message()
async def from_me_to_other(message: Message):
    for key, item in game.allRoomsIsPlaying.items():
        if(message.from_user.id in item):
            to = item[1 - item.index(message.from_user.id)]
            print(to)
            await message.bot.send_message(chat_id=to, text=message.text)
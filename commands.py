from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from game import Game

game = Game()

router = Router()
@router.message(Command('start'))
async def start(message: Message):
    await message.answer('работает')
    #if(reversed(game.allRooms))
    if(game.roomsInWait != {}):
        key, item = list(game.roomsInWait.items())[0] 
        if(len(item) == 1):
            game.roomsInWait[key].append(message.from_user.id)
            await message.answer(str(game.roomsInWait))
            game.allRoomsIsPlaying.update({key: game.roomsInWait[key]})
            del game.roomsInWait[key]
            await message.answer(str(game.roomsInWait))
            await message.answer(str(game.allRoomsIsPlaying))
            await message.bot.send_message(chat_id=game.allRoomsIsPlaying[key][0], text="комната создана")
            await message.bot.send_message(chat_id=game.allRoomsIsPlaying[key][1], text="комната создана")
            
    else:
        print(message.chat.id)
        game.roomsInWait.update({1:[message.from_user.id]})
    

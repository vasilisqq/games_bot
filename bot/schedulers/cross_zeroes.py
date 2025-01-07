from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram.types import ChosenInlineResult
from gameControll.game import game
from bot.keyboards.inline_keyboard import return_to_bot
async def kick_game(query: CallbackQuery|ChosenInlineResult, is_end=False)->None:
    if not is_end:
        await query.bot.edit_message_text(
        text="игра заброшена(",
        inline_message_id=query.inline_message_id,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[return_to_bot]])
        )
    game.crossZeroes.scheduler.remove_job(query.inline_message_id)
    del game.crossZeroes.rooms[query.inline_message_id]

async def kick_open_game(query: CallbackQuery, properties: dict, first: bool = False) -> None:
    counts = 0
    field = properties["keyboard"].inline_keyboard
    for i in range(0,9):
            if i in range (0,3):
                if field[0][i].text != " ":
                    counts += 1
            elif i in range (3,6):
                if field[1][i-3].text != " ":
                    counts +=1
            elif i in range (6,9):
                if field[2][i-6].text != " ":
                    counts+=1
    players = [properties["players"][0][0], properties["players"][1][0]]
    if counts // 2 == 0:
        player = properties["first_player"]
    else:
        player = players[1 - players.index(properties["first_player"])]
    text = (
        f"игру забросил @{player}" 
    )
    if first:
        game.crossZeroes.scheduler.remove_job(properties["players"][0][0])    
    else:
        game.crossZeroes.scheduler.remove_job(query.data[1:])
    await query.bot.edit_message_text(text=text,
                                        chat_id=properties["players"][0][1], 
                                        message_id=properties["message_id"][0])
    await query.bot.edit_message_text(text=text,
                                        chat_id=properties["players"][1][1], 
                                        message_id=properties["message_id"][1])

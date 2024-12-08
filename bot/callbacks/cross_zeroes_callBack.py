from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineQuery
from bot.keyboards.inline_keyboard import create_cross_aeroes
from gameControll.game import game

router = Router()

@router.callback_query(F.data.in_([str(i) for i in range(9)]))
async def mark_button(query: CallbackQuery):
    properties = game.crossZeroes.private_rooms[query.inline_message_id]
    # добавление второго пользователя
    if properties["players"][1] == "" and properties["move"] == "" and properties["players"][0] != query.from_user.username:
        properties["players"][1] = query.from_user.username
        properties["move"] = query.from_user.username
    if properties["move"] == query.from_user.username:
        if properties["first_player"] == query.from_user.username:
            symbol = "X"
        else:
            symbol = "O"
        if(int(query.data) in range(3)):
            properties["keyboard"].inline_keyboard[0][int(query.data)].text = symbol
        if(int(query.data) in range(3,6)):
            properties["keyboard"].inline_keyboard[1][int(query.data)-3].text = symbol
        if(int(query.data) in range(6,9)):
            properties["keyboard"].inline_keyboard[2][int(query.data)-6].text = symbol
        properties["move"] = properties["players"][1 - properties["players"].index(query.from_user.username)]
        if properties["move"] == properties["players"][0]:
            if properties["first_player"] == properties["players"][0]:
                text = (f"игра в крестики-нолики\n\n --> @{properties["players"][0]} X \n @{properties["players"][1]} O")
            else:
                text = (f"игра в крестики-нолики\n\n --> @{properties["players"][0]} O \n @{properties["players"][1]} X")
        else:
            if properties["first_player"] == properties["players"][0]:
                text = (f"игра в крестики-нолики\n\n@{properties["players"][0]} X \n--> @{properties["players"][1]} O")
            else:
                text = (f"игра в крестики-нолики\n\n@{properties["players"][0]} O \n--> @{properties["players"][1]} X")
        await query.bot.edit_message_text(inline_message_id=query.inline_message_id,
                                          text=text, reply_markup=properties["keyboard"])
    else:
        await query.answer("Не твой ход", show_alert=True)
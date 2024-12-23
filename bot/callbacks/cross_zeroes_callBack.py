from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineQuery
from bot.keyboards.inline_keyboard import create_cross_aeroes
from gameControll.game import game
from aiogram.types import InlineKeyboardButton
from bot.schedulers.cross_zeroes import kick_game
router = Router()

@router.callback_query(F.data.in_([str(i) for i in range(9)]))
async def mark_button(query: CallbackQuery):
    properties = game.crossZeroes.private_rooms[query.inline_message_id]
    # добавление второго пользователя
    if properties["players"][1] == "" and properties["move"] == "" and properties["players"][0] != query.from_user.username:
        properties["players"][1] = query.from_user.username
        if properties["first_player"] == "":
            properties["first_player"] = query.from_user.username
        properties["move"] = query.from_user.username
    if properties["move"] == query.from_user.username:
        game.crossZeroes.scheduler.remove_job(query.inline_message_id)
        if properties["first_player"] == query.from_user.username:
            symbol = "X"
        else:
            symbol = "O"
        if int(query.data) in range(3) and properties["keyboard"].inline_keyboard[0][int(query.data)].text == " ":
            properties["keyboard"].inline_keyboard[0][int(query.data)].text = symbol
        elif(int(query.data) in range(3,6)and properties["keyboard"].inline_keyboard[1][int(query.data)-3].text == " "):
            properties["keyboard"].inline_keyboard[1][int(query.data)-3].text = symbol
        elif(int(query.data) in range(6,9) and properties["keyboard"].inline_keyboard[2][int(query.data)-6].text == " "):
            properties["keyboard"].inline_keyboard[2][int(query.data)-6].text = symbol
        else:
            await query.answer("Выбери свободную клетку")
            return
        if await game.crossZeroes.check_win(query.inline_message_id):
            text = f"Победил @{query.from_user.username}"
            await query.bot.edit_message_text(text=text, 
                                              inline_message_id=query.inline_message_id,
                                              reply_markup=properties["keyboard"])
            game.crossZeroes.scheduler.add_job(kick_game,
                                       trigger="interval",
                                       minutes=1,
                                       kwargs = {"query": query, "is_end":True},
                                       id=query.inline_message_id)
        elif await game.crossZeroes.is_draw(query.inline_message_id):
            text = f"Ничья"
            properties["keyboard"].inline_keyboard.append([InlineKeyboardButton(text="заново", 
                                                 callback_data="reload_cross_zeroes_inline")])
            await query.bot.edit_message_text(text=text, 
                                              inline_message_id=query.inline_message_id,
                                              reply_markup=properties["keyboard"])
            game.crossZeroes.scheduler.add_job(kick_game,
                                       trigger="interval",
                                       minutes=1,
                                       kwargs = {"query": query, "is_end":True},
                                       id=query.inline_message_id)
        else:
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
            game.crossZeroes.scheduler.add_job(kick_game,
                                       trigger="interval",
                                       minutes=1,
                                       kwargs = {"query": query},
                                       id=query.inline_message_id)
    else:
        await query.answer("Не твой ход")


@router.callback_query(F.data.in_("reload_cross_zeroes_inline"))
async def reload_game(iquery: CallbackQuery):
    game.crossZeroes.scheduler.remove_job(iquery.inline_message_id)
    game.crossZeroes.scheduler.add_job(kick_game,
                                       trigger="interval",
                                       minutes=1,
                                       kwargs = {"query": iquery},
                                       id=iquery.inline_message_id)
    k = create_cross_aeroes()
    await game.crossZeroes.create__private_room(iquery.from_user.username, k, iquery.inline_message_id, reload=True)
    players = game.crossZeroes.private_rooms[iquery.inline_message_id]["players"]
    await iquery.bot.edit_message_text(inline_message_id=iquery.inline_message_id, 
                                       text=(f"игра в крестики-нолики\n\n --> @{players[0]} X \n @{players[1]} O") if 
                                       game.crossZeroes.private_rooms[iquery.inline_message_id]["first_player"] == players[0] else 
                                       (f"игра в крестики-нолики\n\n @{players[0]} O \n --> @{players[1]} X"),
                                       reply_markup=k)
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineQuery
from bot.keyboards.inline_keyboard import create_cross_aeroes
from gameControll.game import game
from aiogram.types import InlineKeyboardButton
from bot.schedulers.cross_zeroes import kick_game, kick_open_game
from db.DAO import DAO
from bot.bot_configs import set_state
router = Router()

@router.callback_query(F.data[0].in_([str(i) for i in range(9)]))
async def mark_button(query: CallbackQuery):
    if len(query.data) ==1:
        properties = game.crossZeroes.rooms[query.inline_message_id]
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
                game.crossZeroes.scheduler.add_job(kick_game,
                                        trigger="interval",
                                        minutes=1,
                                        kwargs = {"query": query, "is_end":True},
                                        id=query.inline_message_id)
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
    else:
        properties = game.crossZeroes.rooms[query.data[1:]]
        if properties["move"] == query.from_user.username:
            if properties["first_player"][0] == query.from_user.username:
                symbol = "X"
            else:
                symbol = "O"
            if int(query.data[0]) in range(3) and properties["keyboard"].inline_keyboard[0][int(query.data[0])].text == " ":
                properties["keyboard"].inline_keyboard[0][int(query.data[0])].text = symbol
                game.crossZeroes.scheduler.remove_job(query.data[1:])
            elif(int(query.data[0]) in range(3,6)and properties["keyboard"].inline_keyboard[1][int(query.data[0])-3].text == " "):
                properties["keyboard"].inline_keyboard[1][int(query.data[0])-3].text = symbol
                game.crossZeroes.scheduler.remove_job(query.data[1:])
            elif(int(query.data[0]) in range(6,9) and properties["keyboard"].inline_keyboard[2][int(query.data[0])-6].text == " "):
                properties["keyboard"].inline_keyboard[2][int(query.data[0])-6].text = symbol
                game.crossZeroes.scheduler.remove_job(query.data[1:])
            else:
                await query.answer("Выбери свободную клетку")
                # game.crossZeroes.scheduler.add_job(kick_open_game,
                #                        trigger="interval",
                #                        minutes=1,
                #                        kwargs = {"query": query, "properties": game.crossZeroes.rooms[query.data[1:]]},
                #                        id=query.data[1:])
                return
            if await game.crossZeroes.check_win(query.data[1:], in_bot=True):
                await query.bot.edit_message_text(text="вы победили!🥇 \n\n rang +8",
                                                chat_id=query.from_user.id, 
                                                message_id=properties["message_id"][query.from_user.id],
                                                reply_markup=properties["keyboard"])
                await query.bot.edit_message_text(text="вы проебали \n\n rang -8",
                                                  chat_id=properties["players"][1 - properties["players"].index([query.from_user.username, query.from_user.id])][1], 
                                                message_id=properties["message_id"][properties["players"][1 - properties["players"].index([query.from_user.username, query.from_user.id])][1]],
                                                reply_markup=properties["keyboard"])
                await DAO.player_win_and_loose(
                    query.from_user.id,
                    properties["players"][1 - properties["players"].index([query.from_user.username, query.from_user.id])][1])
                await set_state(query.bot, query.from_user.id, "")
                await set_state(query.bot, properties["players"][1 - properties["players"].index([query.from_user.username, query.from_user.id])][1], "")
                del game.crossZeroes.rooms[query.data[1:]]
            elif await game.crossZeroes.is_draw(query.data[1:]):
                text = f"Ничья"
                properties["keyboard"].inline_keyboard.append([InlineKeyboardButton(text="заново", 
                                                    callback_data="reload_cross_zeroes_callback")])
                await query.bot.edit_message_text(text=text,
                                                  chat_id=properties["players"][0][1], 
                                                message_id=properties["message_id"][properties["players"][0][1]],
                                                reply_markup=properties["keyboard"])
                await query.bot.edit_message_text(text=text,
                                                  chat_id=properties["players"][1][1], 
                                                message_id=properties["message_id"][properties["players"][1][1]],
                                                reply_markup=properties["keyboard"])
            else:
                properties["move"] = properties["players"][1 - properties["players"].index([query.from_user.username, query.from_user.id])][0]
                if properties["move"] == properties["players"][0][0]:
                    if properties["first_player"][0] == properties["players"][0][0]:
                        text = (f"игра в крестики-нолики\n\n --> @{properties["players"][0][0]} ({properties["rait"][0]}) X \n @{properties["players"][1][0]} ({properties["rait"][1]}) O")
                    else:
                        text = (f"игра в крестики-нолики\n\n --> @{properties["players"][0][0]} ({properties["rait"][0]}) O \n @{properties["players"][1][0]} ({properties["rait"][1]}) X")
                else:
                    if properties["first_player"][0] == properties["players"][0][0]:
                        text = (f"игра в крестики-нолики\n\n@{properties["players"][0][0]} ({properties["rait"][0]}) X \n--> @{properties["players"][1][0]} ({properties["rait"][1]}) O")
                    else:
                        text = (f"игра в крестики-нолики\n\n@{properties["players"][0][0]} ({properties["rait"][0]}) O \n--> @{properties["players"][1][0]} ({properties["rait"][1]}) X")
                print(properties["message_id"])
                print(properties["players"][0][1])
                await query.bot.edit_message_text(chat_id=properties["players"][0][1],
                                                  message_id=properties["message_id"][properties["players"][0][1]],
                                                text=text, reply_markup=properties["keyboard"])
                await query.bot.edit_message_text(chat_id=properties["players"][1][1],
                                                  message_id=properties["message_id"][properties["players"][1][1]],
                                                text=text, reply_markup=properties["keyboard"])
                game.crossZeroes.scheduler.add_job(kick_open_game,
                                       trigger="interval",
                                       minutes=1,
                                       kwargs = {"query": query, "properties": game.crossZeroes.rooms[query.data[1:]]},
                                       id=query.data[1:])
        else:
            await query.answer("Не твой ход")


@router.callback_query(F.data == "reload_cross_zeroes_inline")
async def reload_game(iquery: CallbackQuery):
    game.crossZeroes.scheduler.remove_job(iquery.inline_message_id)
    game.crossZeroes.scheduler.add_job(kick_game,
                                       trigger="interval",
                                       minutes=1,
                                       kwargs = {"query": iquery},
                                       id=iquery.inline_message_id)
    k = create_cross_aeroes()
    await game.crossZeroes.create__private_room(iquery.from_user.username, k, iquery.inline_message_id, reload=True)
    players = game.crossZeroes.rooms[iquery.inline_message_id]["players"]
    await iquery.bot.edit_message_text(inline_message_id=iquery.inline_message_id, 
                                       text=(f"игра в крестики-нолики\n\n --> @{players[0]} X \n @{players[1]} O") if 
                                       game.crossZeroes.rooms[iquery.inline_message_id]["first_player"] == players[0] else 
                                       (f"игра в крестики-нолики\n\n @{players[0]} O \n --> @{players[1]} X"),
                                       reply_markup=k)
    

@router.callback_query(F.data == "reload_cross_zeroes_callback")
async def new_game_cross_zeroes_in_bot(call: CallbackQuery):
    await call.message.answer("идет поиск противника")
    a = await game.crossZeroes.add_to_listener(call.from_user)
    if a != None:
        m = await call.message.answer(text=a[0],
                                       reply_markup=a[1])
        m1 = await call.bot.send_message(
            chat_id=a[2],
            text=a[0],
            reply_markup=a[1]
        )
        game.crossZeroes.rooms[call.from_user.username]["message_id"] = {
                call.from_user.id:m.message_id, a[2]:m1.message_id}
        game.crossZeroes.scheduler.add_job(kick_open_game,
                                       trigger="interval",
                                       minutes=1,
                                       kwargs = {"query": call, "properties": game.crossZeroes.rooms[call.from_user.username], "first":True},
                                       id=call.from_user.username)
        if not game.crossZeroes.scheduler.running:
            game.crossZeroes.scheduler.start()
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineQuery, InputMediaPhoto
from bot.keyboards.inline_keyboard import create_cross_aeroes
from bot.keyboards.inline_keyboard import return_to_bot
from gameControll.game import game
from aiogram.types import InlineKeyboardButton
from bot.schedulers.cross_zeroes import kick_game, kick_open_game
from db.DAO import DAO
from bot.bot_configs import set_state
from aiogram.fsm.context import FSMContext
from bot.config import settings
import random
from aiogram.types import FSInputFile
from bot.logger import cl
from bot.texts import create_user_name

router = Router()

@router.callback_query(F.data[0].in_([str(i) for i in range(9)]))
async def mark_button(query: CallbackQuery, user):
    if len(query.data) ==1:
        properties = game.crossZeroes.rooms[query.inline_message_id]
        # добавление второго пользователя
        if properties["players"][1] == None and properties["move"] == None and properties["players"][0].user_id != user.user_id:
            properties["players"][1] = user
            if properties["first_player"] == None:
                properties["first_player"] = user
            properties["move"] = user
        if properties["move"].user_id == user.user_id:
            game.crossZeroes.scheduler.remove_job(query.inline_message_id)
            if properties["first_player"].user_id == user.user_id:
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
                cl.custom_logger.info(
                "пользователь выбрал не свою клетку",
                    extra={"username": query.from_user.id,
                    "state": "cleared",
                    "handler_name": "mark_button",
                    "params":f"game: inline, game_id: {query.inline_message_id}"}
                    )
                return
            if await game.crossZeroes.check_win(query.inline_message_id):
                text = f"Победил {create_user_name(user)}"
                await query.bot.edit_message_text(text=text, 
                                                inline_message_id=query.inline_message_id,
                                                reply_markup=properties["keyboard"],
                                                parse_mode="HTML")
                game.crossZeroes.scheduler.add_job(kick_game,
                                        trigger="interval",
                                        minutes=1,
                                        kwargs = {"query": query, "is_end":True},
                                        id=query.inline_message_id)
                cl.custom_logger.info(
                "пользователь выиграл",
                    extra={"username": query.from_user.id,
                    "state": "cleared",
                    "handler_name": "mark_button",
                    "params":f"game: inline, game_id: {query.inline_message_id}"}
                    )
            elif await game.crossZeroes.is_draw(query.inline_message_id):
                text = f"Ничья"
                properties["keyboard"].inline_keyboard.append([InlineKeyboardButton(text="заново", 
                                                    callback_data="reload_cross_zeroes_inline"), return_to_bot])
                await query.bot.edit_message_text(text=text, 
                                                inline_message_id=query.inline_message_id,
                                                reply_markup=properties["keyboard"],
                                                parse_mode="HTML")
                game.crossZeroes.scheduler.add_job(kick_game,
                                        trigger="interval",
                                        minutes=1,
                                        kwargs = {"query": query, "is_end":True},
                                        id=query.inline_message_id)
                cl.custom_logger.info(
                "ничья в игре в крестики нолики",
                    extra={"username": query.from_user.id,
                    "state": "cleared",
                    "handler_name": "mark_button",
                    "params":f"game: inline, game_id: {query.inline_message_id}"}
                    )
            else:
                properties["move"] = properties["players"][1] if properties["players"][0].user_id == user.user_id else properties["players"][0]
                if properties["move"]!= None and properties["move"].user_id == properties["players"][0].user_id:
                    if properties["first_player"].user_id == properties["players"][0].user_id:
                        text = (f"игра в крестики-нолики\n\n --> {create_user_name(properties["players"][0])} X \n {create_user_name(properties["players"][1])} O")
                    else:
                        text = (f"игра в крестики-нолики\n\n --> {create_user_name(properties["players"][0])} O \n {create_user_name(properties["players"][1])} X")
                else:
                    if properties["first_player"].user_id == properties["players"][0].user_id:
                        text = (f"игра в крестики-нолики\n\n {create_user_name(properties["players"][0])} X \n--> {create_user_name(properties["players"][1])} O")
                    else:
                        text = (f"игра в крестики-нолики\n\n {create_user_name(properties["players"][0])} O \n--> {create_user_name(properties["players"][1])} X")
                await query.bot.edit_message_text(inline_message_id=query.inline_message_id,
                                                text=text, reply_markup=properties["keyboard"],
                                                parse_mode="HTML")
                game.crossZeroes.scheduler.add_job(kick_game,
                                        trigger="interval",
                                        minutes=1,
                                        kwargs = {"query": query},
                                        id=query.inline_message_id)
                cl.custom_logger.info(
                f"пользователь сделал ход на клетку {query.data}",
                    extra={"username": query.from_user.id,
                    "state": "cleared",
                    "handler_name": "mark_button",
                    "params":f"game: inline, game_id: {query.inline_message_id}"}
                    )
        else:
            await query.answer("Не твой ход")
    else:
        properties = game.crossZeroes.rooms[query.data[1:]]
        if properties["move"].user_id == query.from_user.id:
            if properties["first_player"].user_id == query.from_user.id:
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
                cl.custom_logger.info(
                "пользователь выбрал занятую клетку клетку",
                    extra={"username": query.from_user.id,
                    "state": "idk",
                    "handler_name": "mark_button",
                    "params":f"game: cb, game_id: {query.data[1:]}"}
                    )
                return
            if await game.crossZeroes.check_win(query.data[1:], in_bot=True):
                await query.bot.edit_message_text(text="🎉 Поздравляю! 🎉 Ты победил! 🥳 \n\n🥇Твой рейтинг:🏆 +8",
                                                chat_id=query.from_user.id, 
                                                message_id=properties["message_id"][query.from_user.id],
                                                reply_markup=properties["keyboard"])
                print(query.from_user.id)
                chat_id = properties["players"][1].user_id if properties["players"][0].user_id == query.from_user.id else properties["players"][0].user_id #!!!!!
                print(chat_id)
                message_id = properties["message_id"][chat_id]
                await query.bot.edit_message_text(text="😢 Увы, ты проиграл. 😞 \n\n🥇Твой рейтинг:🏆 -8",
                                                  chat_id=chat_id, 
                                                message_id=message_id,
                                                reply_markup=properties["keyboard"])
                await DAO.player_win_and_loose(
                    query.from_user.id,
                    chat_id)
                await set_state(query.bot, query.from_user.id, "")
                await set_state(query.bot, chat_id, "")
                del game.crossZeroes.rooms[query.data[1:]]
                cl.custom_logger.info(
                "пользователь победил",
                    extra={"username": query.from_user.id,
                    "state": "idk",
                    "handler_name": "mark_button",
                    "params":f"game: cb, game_id: {query.data[1:]}"}
                    )
            elif await game.crossZeroes.is_draw(query.data[1:]):
                text = f"Ничья"
                properties["keyboard"].inline_keyboard.append([InlineKeyboardButton(text="заново", 
                                                    callback_data="reload_cross_zeroes_callback")])
                img = f"{settings.HOME_PATH}/medias/photos/draw/{random.randint(1,9)}.jpg"
                await query.bot.delete_message(
                    properties["players"][0].user_id,
                    message_id=properties["message_id"][properties["players"][0].user_id]
                )
                await query.bot.delete_message(
                    properties["players"][1].user_id,
                    message_id=properties["message_id"][properties["players"][1].user_id]
                )
                await query.bot.send_photo(
                            properties["players"][0].user_id,
                            FSInputFile(img),
                            reply_markup=properties["keyboard"]
    )
                await query.bot.send_photo(
                            properties["players"][1].user_id,
                            FSInputFile(img),
                            reply_markup=properties["keyboard"]
    )
                
                await set_state(query.bot, properties["players"][0].user_id, "")
                await set_state(query.bot, properties["players"][1].user_id, "")
                cl.custom_logger.info(
                "ничья",
                    extra={"username": query.from_user.username,
                    "state": "idk",
                    "handler_name": "mark_button",
                    "params":f"game: cb, game_id: {query.data[1:]}"}
                    )
            else:
                # properties["move"] = properties["players"][1 - properties["players"].index([query.from_user.username, query.from_user.id])][0] #### !!!!!!!!!!!!!!!!!!!!!!!
                properties["move"] = properties["players"][1] if properties["players"][0].user_id == user.user_id else properties["players"][0]
                if properties["move"].user_id == properties["players"][0].user_id:
                    if properties["first_player"].user_id == properties["players"][0].user_id:
                        text = (f"игра в крестики-нолики\n\n --> {create_user_name(properties["players"][0])} ({properties["rait"][0]}) X \n {create_user_name(properties["players"][1])} ({properties["rait"][1]}) O")
                    else:
                        text = (f"игра в крестики-нолики\n\n --> {create_user_name(properties["players"][0])} ({properties["rait"][0]}) O \n {create_user_name(properties["players"][1])} ({properties["rait"][1]}) X")
                else:
                    if properties["first_player"].user_id == properties["players"][0].user_id:
                        text = (f"игра в крестики-нолики\n\n {create_user_name(properties["players"][0])} ({properties["rait"][0]}) X \n--> {create_user_name(properties["players"][1])} ({properties["rait"][1]}) O")
                    else:
                        text = (f"игра в крестики-нолики\n\n {create_user_name(properties["players"][0])} ({properties["rait"][0]}) O \n--> {create_user_name(properties["players"][1])} ({properties["rait"][1]}) X")
                await query.bot.edit_message_text(chat_id=properties["players"][0].user_id,
                                                  message_id=properties["message_id"][properties["players"][0].user_id],
                                                text=text, reply_markup=properties["keyboard"],
                                                parse_mode="HTML")
                await query.bot.edit_message_text(chat_id=properties["players"][1].user_id,
                                                  message_id=properties["message_id"][properties["players"][1].user_id],
                                                text=text, reply_markup=properties["keyboard"],
                                                parse_mode="HTML")
                game.crossZeroes.scheduler.add_job(kick_open_game,
                                       trigger="interval",
                                       minutes=1,
                                       kwargs = {"query": query, "properties": game.crossZeroes.rooms[query.data[1:]], "user":user},
                                       id=query.data[1:])
                cl.custom_logger.info(
                f"пользователь сделал ход на клетку {query.data[0]}",
                    extra={"username": query.from_user.id,
                    "state": "idk",
                    "handler_name": "mark_button",
                    "params":f"game: cb, game_id: {query.data[1:]}"}
                    )
        else:
            await query.answer("Не твой ход")


@router.callback_query(F.data == "reload_cross_zeroes_inline")
async def reload_game(iquery: CallbackQuery, user):
    game.crossZeroes.scheduler.remove_job(iquery.inline_message_id)
    game.crossZeroes.scheduler.add_job(kick_game,
                                       trigger="interval",
                                       minutes=1,
                                       kwargs = {"query": iquery},
                                       id=iquery.inline_message_id)
    k = create_cross_aeroes()
    await game.crossZeroes.create__private_room(user, k, iquery.inline_message_id, reload=True)
    players = game.crossZeroes.rooms[iquery.inline_message_id]["players"]
    await iquery.bot.edit_message_text(inline_message_id=iquery.inline_message_id, 
                                       text=(f"игра в крестики-нолики\n\n --> {create_user_name(players[0])} X \n {create_user_name(players[1])} O") if 
                                       game.crossZeroes.rooms[iquery.inline_message_id]["first_player"].user_id == players[0].user_id else 
                                       (f"игра в крестики-нолики\n\n {create_user_name(players[1])} O \n --> {create_user_name(players[1])} X"),
                                       reply_markup=k,
                                       parse_mode="HTML")
    cl.custom_logger.info(
                "пользователь начал игру в крестики нолики заново",
                    extra={"username": iquery.from_user.id,
                    "state": "idk",
                    "handler_name": "reload_game",
                    "params":f"game: inline, game_id: {iquery.inline_message_id}"}
                    )
    

@router.callback_query(F.data == "reload_cross_zeroes_callback")
async def new_game_cross_zeroes_in_bot(call: CallbackQuery, state: FSMContext, user):
    a:dict[str, str] = await state.get_data()
    # print(a)
    if a == {} or not a["state"].startswith("in_game"):
        await call.message.answer("идет поиск противника")
        a = await game.crossZeroes.add_to_listener(user)
        await state.update_data(state="in_game_cross_zeroes")
        if a != None:
            m = await call.message.answer(text=a[0],
                                        reply_markup=a[1],
                                        parse_mode="HTML")
            m1 = await call.bot.send_message(
                chat_id=a[2],
                text=a[0],
                reply_markup=a[1],
                parse_mode="HTML"
            )
            game.crossZeroes.rooms[str(call.from_user.id)]["message_id"] = {
                    call.from_user.id:m.message_id, a[2]:m1.message_id}
            game.crossZeroes.scheduler.add_job(kick_open_game,
                                        trigger="interval",
                                        minutes=1,
                                        kwargs = {"query": call, "properties": game.crossZeroes.rooms[str(call.from_user.id)],"user":user, "first":True},
                                        id=str(call.from_user.id))
            if not game.crossZeroes.scheduler.running:
                game.crossZeroes.scheduler.start()
        cl.custom_logger.info(
                "пользователь начал поиск в крестики нолики",
                    extra={"username": call.from_user.id,
                    "state": "idk",
                    "handler_name": "new_game_cross_zeroes_in_bot",
                    "params":f"game: cb, game_id: none"}
                    )
    else:
        await call.answer("у тебя есть игра, закончи ее прежде, чем начинать новую", show_alert=True)
        cl.custom_logger.info(
                "пользователь попытался начать игру, но уже имеет текущую",
                    extra={"username": call.from_user.id,
                    "state": "idk",
                    "handler_name": "new_game_cross_zeroes_in_bot",
                    "params":f"game: cb, game_id: {call.inline_message_id}"}
                    )
        
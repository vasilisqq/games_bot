from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from bot.keyboards.inline_keyboard import friend_or_alone, friend_or_alone_ni
from bot.keyboards.reply_keyboard import cancel_btn
from gameControll.game import game
from bot.schedulers.cross_zeroes import kick_open_game
from bot.config import settings
from bot.texts import instruction_text
from aiogram.fsm.context import FSMContext
from bot.bot_configs import get_state, set_state
import logging

router = Router()

@router.callback_query(F.data == "cross-zeroes")
async def choose_mate_inline_games(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.delete()
    a:dict[str, str] = await state.get_data()
    if a == {} or not a["state"].startswith("in_game"):
        await state.update_data(state=call.data)
    await call.message.answer_photo(
        photo=FSInputFile(f"{settings.HOME_PATH}/medias/photos/instruction.jpg"),
        caption=instruction_text
    )
    await call.message.answer("Играть одному или с другом?",
                              reply_markup=friend_or_alone)
    logging.info(
                f"пользователь нажал на кнопку крестиков ноликов",
                    extra={"username": call.from_user.username,
                    "state": await state.get_data(),
                    "handler_name": "choose_mate_inline_games",
                    "params":"nothing"}
                    )


@router.callback_query(F.data == "wordlie")
async def choose_mate(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    a:dict[str, str] = await state.get_data()
    if a == {} or not a["state"].startswith("in_game"):
        await state.update_data(state=call.data)
        await call.message.answer("Играть одному или с другом?",
                              reply_markup=friend_or_alone_ni)
        logging.info(
                f"пользователь нажал на кнопку вордли",
                    extra={"username": call.from_user.username,
                    "state": await state.get_data(),
                    "handler_name": "choose_mate",
                    "params":"nothing"}
                    )
    else:
        await call.message.answer("у тебя есть игра, закончи ее прежде, чем начинать новую")
        logging.info(
                f"пользователь попытался войти в вордли, но у него есть начатая игра",
                    extra={"username": call.from_user.username,
                    "state": await state.get_data(),
                    "handler_name": "choose_mate",
                    "params":"nothing"}
                    )

@router.callback_query(F.data == "game_alone")
async def alone_game(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    a:dict[str, str] = await state.get_data()
    if a["state"].startswith("in_game"):
        await call.message.answer("у тебя есть игра, закончи ее прежде, чем начинать новую")
        logging.info(
                f"пользователь попытался поиграть в крестики-нолики один, но у него уже ест игра",
                    extra={"username": call.from_user.username,
                    "state": await state.get_data(),
                    "handler_name": "alone_game",
                    "params":"nothing"}
                    )
    else:
        await call.message.answer("идет поиск противника")
        a = await game.crossZeroes.add_to_listener(call.from_user)
        await state.update_data(state="in_game_cross_zeroes")
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
        logging.info(
                f"пользователь начал поиск игры в крестики-нолики",
                    extra={"username": call.from_user.username,
                    "state": await state.get_data(),
                    "handler_name": "alone_game",
                    "params":"nothing"}
                    )
            
@router.callback_query(F.data == "game_alone_")
async def create_alone_room(call: CallbackQuery, state: FSMContext):
    a:dict[str, str] = await state.get_data()
    if a== {} or a["state"].startswith(("in_game", "f_in_game")):
        await call.message.answer("закончи уже начатую игру")
        logging.info(
                f"пользователь попытался запустить одиночный wordlie, но у него уже есть игра",
                    extra={"username": call.from_user.username,
                    "state": await state.get_data(),
                    "handler_name": "create_alone_room",
                    "params":"nothing"}
                )
    else:
        await call.message.delete()
        await game.wordlie.create_alone_game(call.from_user.id)
        await state.update_data(state="in_game_wordlie")
        await call.message.answer("Введите слово")
        await state.set_state(game.state)
        logging.info(
                f"пользователь начал игру в wordlie",
                    extra={"username": call.from_user.username,
                    "state": await state.get_data(),
                    "handler_name": "choose_mate",
                    "params":"nothing"}
                    )

@router.callback_query(F.data == "with_friend")
async def create_word_for_friend(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Введи username без собачки своего друга, а через пробел введи загаданное слово \n\n чтобы выйти отсюда напиши 'отмена' ",
                              reply_markup=cancel_btn)
    await state.set_state(game.wordlie.send_word)
    logging.info(
                f"пользователь начал загадывать слово другу в wordlie",
                    extra={"username": call.from_user.username,
                    "state": await state.get_data(),
                    "handler_name": "choose_mate",
                    "params":"nothing"}
                    )
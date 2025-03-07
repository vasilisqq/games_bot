from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from gameControll.game import game
from bot.logger import cl
from bot.texts import create_user_name

router = Router()
@router.callback_query(F.data == "wordlie_from_friend")
async def game_wordlie_from_friend(call: CallbackQuery, state: FSMContext):
    a:dict = await state.get_data()
    if a == {} or not a["state"].startswith(("in_game", "f_in_game")):
        await call.message.delete()
        await state.update_data(state="f_in_game_wordlie")
        await call.message.answer("Введите слово")
        await state.set_state(game.state)
        cl.custom_logger.info(
                    f"пользователь принял вордли игру от друга",
                        extra={"username": call.from_user.id,
                        "state": await state.get_data(),
                        "handler_name": "game_wordlie_from_friend",
                        "params":"nothing"}
                        )
    else:
        await call.message.answer("Закончи игру, прежде чем начинат новую")
        cl.custom_logger.info(
                    f"пользователь пытался начать игру вордли от друга, но у него уже есть начатая игра",
                        extra={"username": call.from_user.id,
                        "state": await state.get_data(),
                        "handler_name": "game_wordlie_from_friend",
                        "params":"nothing"}
                        )
    



@router.callback_query(F.data == "wordlie_diss")
async def disconnect(call: CallbackQuery, user):
    await call.message.delete()
    await call.message.answer("Вы отклонили запрос на игру")
    await call.bot.send_message(
        chat_id=game.wordlie.rooms[call.from_user.id]["sender"],
        text=f"игрок {create_user_name(user)} отклонил игру",
        parse_mode="HTML"
    )
    del game.wordlie.rooms[call.from_user.id]
    cl.custom_logger.info(
                f"пользователь отклонил игру в вордли от друга",
                    extra={"username": call.from_user.id,
                    "state": "nothing",
                    "handler_name": "disconnect",
                    "params":"nothing"}
                    )

from secrets import token_hex
from aiogram import Router
from aiogram.types import (
    InlineQuery,
    InlineQueryResultPhoto,
    InputTextMessageContent,
    ChosenInlineResult
)
from bot.keyboards.inline_keyboard import create_cross_aeroes
from gameControll.game import game
from bot.schedulers.cross_zeroes import kick_game
from bot.logger import cl
from bot.texts import create_user_name

router = Router()
keyboard = create_cross_aeroes()


#обработка inline запроса
@router.inline_query()
async def new_user(iquery: InlineQuery) -> None:
    random_id = token_hex(2)
    print(random_id)
    keyboard = create_cross_aeroes()
    await iquery.answer([
        InlineQueryResultPhoto(
            id = random_id,
            photo_url="https://i.ibb.co/StnJn5g/cross-zeroes-big.png",
            thumbnail_url="https://i.ibb.co/hMRs6j4/cross-zeroes.png",
            photo_height=100,
            photo_width=100,
            input_message_content=InputTextMessageContent(
                message_text=(f"игра в крестики-нолики \n\n подождите чуть-чуть"),
            ),
            reply_markup=keyboard
        )
    ],
    is_personal=False,
    cache_time=1)
    cl.custom_logger.info(
        "пользователь тегнул бота в чате",
        extra={"username": iquery.from_user.id,
               "state": "None",
               "handler_name": "new_user",
               "params":"{}"}
    )


#сюда приходит то, что пользователь отправил в предыдущем запросе
@router.chosen_inline_result()
async def f(iquery: ChosenInlineResult,user) -> None:
    k = create_cross_aeroes()
    await game.crossZeroes.create__private_room(user, k, iquery.inline_message_id)
    await iquery.bot.edit_message_text(inline_message_id=iquery.inline_message_id, 
                                       text=(f'игра в крестики-нолики\n\n --> {create_user_name(user)} X \n ? O') if 
                                       game.crossZeroes.rooms[iquery.inline_message_id]["first_player"] is not None else 
                                       (f'игра в крестики-нолики\n\n {create_user_name(user)} O \n --> ? X'),
                                       reply_markup=k,
                                       parse_mode="HTML")
    game.crossZeroes.scheduler.add_job(kick_game,
                                       trigger="interval",
                                       minutes=1,
                                       kwargs = {"query": iquery},
                                       id=iquery.inline_message_id)
    if not game.crossZeroes.scheduler.running:
        game.crossZeroes.scheduler.start()
    cl.custom_logger.info(
        f"пользователь выбрал что-то",
        extra={"username": iquery.from_user.id,
               "state": "None",
               "handler_name": "f",
               "params":iquery.result_id}
    )
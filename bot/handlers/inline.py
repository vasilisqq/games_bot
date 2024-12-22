from secrets import token_hex
from typing import Any
from aiogram import Router
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InputTextMessageContent,
    ChosenInlineResult,
    LinkPreviewOptions
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db.models.user import Users
from bot.keyboards.inline_keyboard import create_cross_aeroes
from gameControll.game import game
from bot.schedulers.cross_zeroes import kick_game
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
                message_text=(f"игра в крестики-нолики\n\n @{iquery.from_user.username}"),
            ),
            reply_markup=keyboard
        )
    ],
    is_personal=False,
    cache_time=1)


#сюда приходит то, что пользователь отправил в предыдущем запросе
@router.chosen_inline_result()
async def f(iquery: ChosenInlineResult) -> None:
    k = create_cross_aeroes()
    await game.crossZeroes.create__private_room(iquery.from_user.username, k, iquery.inline_message_id)
    print(game.crossZeroes.private_rooms[iquery.inline_message_id]["first_player"])
    await iquery.bot.edit_message_text(inline_message_id=iquery.inline_message_id, 
                                       text=(f"игра в крестики-нолики\n\n --> @{iquery.from_user.username} X \n ? O") if 
                                       game.crossZeroes.private_rooms[iquery.inline_message_id]["first_player"] == iquery.from_user.username else 
                                       (f"игра в крестики-нолики\n\n @{iquery.from_user.username} O \n --> ? X"),
                                       reply_markup=k)
    game.crossZeroes.scheduler.add_job(kick_game,
                                       trigger="interval",
                                       minutes=1,
                                       kwargs = {"query": iquery},
                                       id=iquery.inline_message_id)
    game.crossZeroes.scheduler.start()
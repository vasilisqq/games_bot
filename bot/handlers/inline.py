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

router = Router()

#обработка inline запроса
@router.inline_query()
async def new_user(iquery: InlineQuery) -> None:
    random_id = token_hex(2)
    markup = (
        InlineKeyboardBuilder()
        .button(text="кнопка", callback_data="w_")
    )
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
            reply_markup=create_cross_aeroes()
        )
    ],
    is_personal=False,
    cache_time=1)
    # await iquery.answer([
    #     InlineQueryResultArticle(
    #     id=random_id,
    #     title="врлоываровыплл",
    #     description="КИРИЛЛ",
    #     input_message_content=InputTextMessageContent(
    #         message_text=(
    #             "покемончик"
    #         ),
    #         link_preview_option=LinkPreviewOptions(is_disabled=True),
    #         disable_web_page_preview=True
    #     ),
    #     reply_markup= markup.as_markup()
    #     )
    # ],
    # cache_time=1,
    # #можно использовать запросы в не бота
    # is_presonal = False
    # )

#сюда приходит то, что пользователь отправил в предыдущем запросе
@router.chosen_inline_result()
async def f(iquery: ChosenInlineResult) -> None:
    ...

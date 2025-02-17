from aiogram.types import Message
from aiogram import Router
from bot.keyboards.inline_keyboard import choose_game, show_top
from bot.logger import cl

router = Router()

@router.message()
async def helper_in_menu(message: Message):
    if message.text == "Выбор игры":
        await message.answer("Выбери игру, в которую хочешь поиграть",
                       reply_markup=choose_game)
    elif message.text == "Сильнейшие игроки💪":
        await message.answer("Выбери игру по которой хочешь посомтреть топ игроков",
                             reply_markup=show_top)
    elif message.text == "Настройки⚙️":
        await message.answer("soon")
    else:
        await message.answer("используй кнопки, чтобы перемещаться по боту")
    cl.custom_logger.info(
        "пользоваатель написал сообщение",
        extra={"username": message.from_user.username,
               "state": "None",
               "handler_name": "helper_in_menu",
               "params":message.text}
    )
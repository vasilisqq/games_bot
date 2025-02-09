from aiogram.types import Message
from aiogram import Router
from bot.keyboards.inline_keyboard import choose_game, show_top

router = Router()

@router.message()
async def helper_in_menu(message: Message):
    if message.text == "Выбор игры":
        await message.answer("Выбери игру, в которую хочешь поиграть",
                       reply_markup=choose_game)
    if message.text == "Сильнейшие игроки💪":
        await message.answer("Выбери игру по которой хочешь посомтреть топ игроков",
                             reply_markup=show_top)
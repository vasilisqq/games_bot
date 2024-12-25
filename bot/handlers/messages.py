from aiogram.types import Message
from aiogram import Router
from bot.keyboards.inline_keyboard import choose_game

router = Router()

@router.message()
async def helper_in_menu(message: Message):
    if message.text == "выбор игры":
        await message.answer("Выбери игру в которую хочешь поиграть:",
                       reply_markup=choose_game)
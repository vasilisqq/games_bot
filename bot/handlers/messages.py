from aiogram.types import Message
from aiogram import Router
from bot.keyboards.inline_keyboard import choose_game, friend_or_alone

router = Router()

@router.message()
async def helper_in_menu(message: Message):
    if message.text == "выбор игры":
        await message.answer("Выбери с кем хочешь поиграть",
                       reply_markup=friend_or_alone)
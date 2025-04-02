from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from gameControll.game import game

router = Router()


@router.message(Command("start_game"), F.chat.type.in_({"group", "supergroup"}))
async def answer_in_group(message: Message):
    game.create_mafia_game(
        message.chat.id,
        message.from_user.id)
    await message.answer(
        "нажми на кнопку ниже, чтобы зарегестрироваться на игру",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="присоединиться к игре", callback_data="join_to_mafia_game")
                ]
            ]
        ))


@router.message(F.text.startswith("/"))
async def unknown_command_handler(message: Message):
    await message.answer("Неизвестная команда. Пожалуйста, проверьте правильность ввода команды.")    

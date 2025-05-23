from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from gameControll.game import game
from bot.keyboards.inline_keyboard import create_join_button
from bot.texts import create_user_name

router = Router()


@router.message(Command("start_game"), F.chat.type.in_({"group", "supergroup"}))
async def answer_in_group(message: Message, user):
    await message.delete()
    mes = await message.answer(
        "нажми на кнопку ниже, чтобы зарегестрироваться на игру\n\n"+
        f"{create_user_name(user)}",
        parse_mode="HTML",
        reply_markup=await create_join_button(message.chat.id, message.chat.full_name))
    await game.create_mafia_game(
        message.chat.id,
        user,
        message.bot,
        mes.message_id)


@router.message(F.text.startswith("/"))
async def unknown_command_handler(message: Message):
    await message.answer("Неизвестная команда. Пожалуйста, проверьте правильность ввода команды.")    

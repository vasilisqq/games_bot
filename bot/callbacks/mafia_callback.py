from aiogram import Router, F
from aiogram.types import CallbackQuery
from gameControll.game import game
from bot.texts import create_user_name
from bot.keyboards.inline_keyboard import create_join_button
router = Router()

@router.callback_query(F.data == "join_to_mafia_game")
async def join_to_mafia_room(query: CallbackQuery, user) -> None:
    ...
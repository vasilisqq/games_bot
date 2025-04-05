from aiogram import Router, F
from aiogram.types import CallbackQuery
from gameControll.game import game
from bot.texts import create_user_name
router = Router()

@router.callback_query(F.data == "join_to_mafia_game")
async def join_to_mafia_room(query: CallbackQuery, user) -> None:
    message = query.message
    text = message.text
    query.bot.edit_message_text(
        text=text + f"{create_user_name(user)}\n",
        chat_id=message.chat.id,
        message_id=message.id,
        parse_mode="HTML"
    )
from aiogram import Router, F
from aiogram.types import CallbackQuery
from gameControll.game import game
from bot.texts import create_user_name
from bot.keyboards.inline_keyboard import join_mafia_game
router = Router()

@router.callback_query(F.data == "join_to_mafia_game")
async def join_to_mafia_room(query: CallbackQuery, user) -> None:
    message = query.message
    is_added = game.add_user_in_mafia_game(message.chat.id, query.from_user.id)
    text = "нажми на кнопку ниже, чтобы зарегестрироваться на игру\n\n"
    if is_added:
        for item in is_added:
            text += create_user_name()
    await query.bot.edit_message_text(
        text=text + f"\n{create_user_name(user)}",
        chat_id=message.chat.id,
        message_id=message.message_id,
        parse_mode="HTML",
        reply_markup=join_mafia_game
    )
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram.types import ChosenInlineResult
from bot.keyboards.inline_keyboard import return_to_bot
async def kick_game(query: CallbackQuery|ChosenInlineResult):
    print("A")
    print(query.inline_message_id)
    await query.bot.edit_message_text(
        text="игра заброшена(",
        inline_message_id=query.inline_message_id,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[return_to_bot]])
    )
    print("B")
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram.types import ChosenInlineResult
from gameControll.game import game
from bot.keyboards.inline_keyboard import return_to_bot
async def kick_game(query: CallbackQuery|ChosenInlineResult, is_end=False)->None:
    if not is_end:
        await query.bot.edit_message_text(
        text="игра заброшена(",
        inline_message_id=query.inline_message_id,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[return_to_bot]])
        )
    game.crossZeroes.scheduler.remove_job(query.inline_message_id)
    del game.crossZeroes.private_rooms[query.inline_message_id]

async def kick_open_game(query: CallbackQuery) -> None:
    # query.bot
    pass

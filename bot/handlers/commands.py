from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from bot.texts import start_text
from bot.config import settings
from bot.keyboards.reply_keyboard import choose_game_or_else
router = Router()


@router.message(Command("start"))
async def start_bot(message: Message):
    await message.answer_animation(
        animation=FSInputFile(f"{settings.HOME_PATH}/medias/gifs/start.mp4"),
        caption=start_text,
        reply_markup=choose_game_or_else,
        message_effect_id="5159385139981059251"
    )
    # await message.answer_photo(
    #     photo=FSInputFile(f"{settings.HOME_PATH}/medias/photos/start.jpg"),
    #     caption=start_text,
    #     reply_markup=choose_game_or_else
    # )
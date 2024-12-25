from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from bot.texts import start_text
from bot.config import settings
router = Router()


@router.message(Command("start"))
async def start_bot(message: Message):
    await message.answer_photo(
        photo=FSInputFile(f"{settings.HOME_PATH}/medias/photos/start.jpg"),
        caption=start_text
    )
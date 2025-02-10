import logging
from aiogram import Bot
from aiogram.types import FSInputFile
from bot.config import settings

class Logger():
# Настройка логгеров
    logging.basicConfig(level=logging.DEBUG)

    # Логгер для DEBUG
    debug_logger = logging.getLogger("debug_logger")
    debug_logger.setLevel(logging.DEBUG)
    debug_handler = logging.FileHandler("debug.log")
    debug_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    debug_logger.addHandler(debug_handler)

    # Логгер для INFO
    info_logger = logging.getLogger("info_logger")
    info_logger.setLevel(logging.INFO)
    info_handler = logging.FileHandler("info.log")
    info_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    info_logger.addHandler(info_handler)

    # Логгер для ERROR/CRITICAL
    error_logger = logging.getLogger("error_logger")
    error_logger.setLevel(logging.ERROR)

    async def send_error_to_admin(self, bot: Bot, error_message: str):
        await bot.send_message(settings.ADMIN_ID, f"🚨 Ошибка в боте:\n{error_message}")
        f = FSInputFile(f"{settings.HOME_PATH}/info.log", filename="info.log")
        await bot.send_document(
            settings.ADMIN_ID,
            f
        )
logger = Logger()
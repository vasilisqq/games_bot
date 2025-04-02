import logging
from bot.config import settings
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime 
import os
from aiogram.types import FSInputFile
# print()

class CustomLogger:
    def __init__(self) -> None:
    
        self.aiogram_logger = logging.getLogger("aiogram")
        self.aiogram_logger.setLevel(logging.DEBUG)
        self.aiogram_handler = logging.StreamHandler()
        self.aiogram_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        self.aiogram_logger.addHandler(self.aiogram_handler)
        self.schedule = AsyncIOScheduler(timezone="Europe/Moscow")
        self.custom_logger = logging.getLogger("my_bot")
        self.custom_logger.setLevel(logging.DEBUG)
        self.custom_handler = logging.FileHandler(f"{settings.HOME_PATH}/{datetime.date.today()}.log")
        self.custom_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(username)s - %(state)s - %(handler_name)s - %(params)s"
        ))
        self.custom_logger.addHandler(self.custom_handler)


    async def send_logs_to_admin(self, bot:Bot) -> None:
        self.custom_handler = logging.FileHandler(f"{settings.HOME_PATH}/{datetime.date.today()}.log")
        await bot.send_document(
            settings.ADMIN_ID,
            FSInputFile(f"{settings.HOME_PATH}/{datetime.date.today() - datetime.date.day(1)}.log"), 
            caption="Логи за день")
        bot.logger.info("Логи отправлены администратору.")
        os.remove(f"{settings.HOME_PATH}/{datetime.date.today() - datetime.date.day(1)}.log")

cl = CustomLogger()

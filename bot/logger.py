import logging
from bot.config import settings
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime 
import os
# print()

class CustomLogger:
    def __init__(self) -> None:
    
        # Логгер для aiogram
        self.aiogram_logger = logging.getLogger("aiogram")
        self.aiogram_logger.setLevel(logging.DEBUG)
        # self.aiogram_handler = logging.FileHandler(f"{settings.HOME_PATH}/aiogram.log")
        # self.aiogram_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        # self.aiogram_logger.addHandler(self.aiogram_handler)
        self.aiogram_handler = logging.StreamHandler()
        self.aiogram_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        self.aiogram_logger.addHandler(self.aiogram_handler)
        self.schedule = AsyncIOScheduler(timezone="Europe/Moscow")
        # Логгер для вашего кода
        self.custom_logger = logging.getLogger("my_bot")
        self.custom_logger.setLevel(logging.DEBUG)
        self.custom_handler = logging.FileHandler(f"{settings.HOME_PATH}/{datetime.date.today()}.log")
        self.custom_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(username)s - %(state)s - %(handler_name)s - %(params)s"
        ))
        self.custom_logger.addHandler(self.custom_handler)


    async def send_logs_to_admin(self, bot:Bot) -> None:
        with open("bot.log", "rb") as log_file:
            await bot.send_document(settings.ADMIN_ID, log_file, caption="Логи за день")
            bot.logger.info("Логи отправлены администратору.")
            log_file.close()
            if os.path.exists(f"{settings.HOME_PATH}/{datetime.date.today() - datetime.date.day(1)}.log"):
                os.remove(f"{settings.HOME_PATH}/{datetime.date.today() - datetime.date.day(1)}.log")
        self.custom_handler = logging.FileHandler(f"{settings.HOME_PATH}/{datetime.date.today() + datetime.datetime.day(1)}.log")

cl = CustomLogger()

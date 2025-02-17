import logging
from bot.config import settings

class CustomLogger:
    def __init__(self) -> None:
    
        # Логгер для aiogram
        self.aiogram_logger = logging.getLogger("aiogram")
        self.aiogram_logger.setLevel(logging.DEBUG)
        self.aiogram_handler = logging.FileHandler(f"{settings.HOME_PATH}/aiogram.log")
        self.aiogram_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        self.aiogram_logger.addHandler(self.aiogram_handler)
        self.aiogram_handler = logging.StreamHandler()
        self.aiogram_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        self.aiogram_logger.addHandler(self.aiogram_handler)

        # Логгер для вашего кода
        self.custom_logger = logging.getLogger("my_bot")
        self.custom_logger.setLevel(logging.DEBUG)
        self.custom_handler = logging.FileHandler(f"{settings.HOME_PATH}/bot.log")
        self.custom_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(username)s - %(state)s - %(handler_name)s - %(params)s"
        ))
        self.custom_logger.addHandler(self.custom_handler)

cl = CustomLogger()

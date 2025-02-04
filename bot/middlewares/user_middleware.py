from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Update
from db.DAO import DAO

# dao = DAO()

# создаю класс для создания своего middleware
class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        #        есть какаято функция которой мы передаем Update и какие то данные в dict и вызывается это все асинхронно
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any]
    ) -> Any:
        current_evenr = (
            event.message
            or event.callback_query
            or event.inline_query
            or event.chosen_inline_result
        )
        if not current_evenr:
            return
        await DAO.create_and_return_user(current_evenr.from_user.id, current_evenr.from_user.username)
        return await handler(event, data)
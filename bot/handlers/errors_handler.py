from aiogram import Router
from aiogram.types import ErrorEvent
from bot.logger import logger
from aiogram.fsm.context import FSMContext

router = Router()
@router.error()
async def print_error(event: ErrorEvent, state: FSMContext):
    text = (
        f"у пользователя {event.update.message.from_user.username} произошла ошибка {event.exception}/n"+
        f"его состояние: {await state.get_data()}"
    )
    await logger.send_error_to_admin(
        event.update.bot,
        text
    )
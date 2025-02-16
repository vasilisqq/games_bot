from aiogram import Router
from aiogram.types import ErrorEvent, FSInputFile
from aiogram.fsm.context import FSMContext
from bot.config import settings

router = Router()
@router.error()
async def print_error(event: ErrorEvent, state: FSMContext):
    try:
        text = (
            f"у пользователя {event.update.message.from_user.username} произошла ошибка {event.exception}/n"+
            f"его состояние: {await state.get_data()}"
        )
    except:
        try:
            text = (
            f"у пользователя {event.update.callback_query.from_user.username} произошла ошибка {event.exception}/n"+
            f"его состояние: {await state.get_data()}"
        )
        except:
            text = (
            f"у пользователя {event.update.inline_query.from_user.username} произошла ошибка {event.exception}/n"+
            f"его состояние: {await state.get_data()}"
        )
    event.update.bot.send_message(
        chat_id=settings.ADMIN_ID,
        text=text
    )
    event.update.bot.send_document(
        chat_id=settings.ADMIN_ID,
        document=FSInputFile(f"{settings.HOME_PATH}/bot.log"),
        caption=text
    )
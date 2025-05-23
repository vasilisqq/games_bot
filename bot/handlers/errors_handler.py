from aiogram import Router
from aiogram.types import ErrorEvent, FSInputFile
from aiogram.fsm.context import FSMContext
from bot.config import settings
import traceback
import datetime

router = Router()
@router.error()
async def print_error(event: ErrorEvent, state: FSMContext):
    with open(f"{settings.HOME_PATH}/trace_back.txt", "w") as f:
        f.write(traceback.format_exc())
        f.close()
    try:
        text = (
            f"у пользователя {event.update.message.from_user.username} произошла ошибка {event.exception} \n"+
            f"его состояние: {await state.get_data()}"
        )
    except:
        try:
            text = (
            f"у пользователя {event.update.callback_query.from_user.username} произошла ошибка {event.exception}\n"
        )
        except:
            try:
                text = (
                f"у пользователя {event.update.inline_query.from_user.username} произошла ошибка {event.exception} \n"+
                f"его состояние: {await state.get_data()}"
                )
            except:
                text = (
                f"у пользователя {event.update.chosen_inline_result.from_user.username} произошла ошибка {event.exception} \n"+
                f"его состояние: {await state.get_data()}"
                )
    # await event.update.bot.send_message(
    #     chat_id=settings.ADMIN_ID,
    #     text=text
    # )
    await event.update.bot.send_document(
        chat_id=settings.ADMIN_ID,
        document=FSInputFile(f"{settings.HOME_PATH}/{datetime.date.today()}.log"),
        caption=text
    )
    await event.update.bot.send_document(
        chat_id=settings.ADMIN_ID,
        document=FSInputFile(f"{settings.HOME_PATH}/trace_back.txt")
    )
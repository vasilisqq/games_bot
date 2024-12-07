from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data.in_(str(range(9))))
async def mark_button(query: CallbackQuery):
    print(query)
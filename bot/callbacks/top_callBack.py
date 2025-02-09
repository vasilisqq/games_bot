from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from gameControll.game import game
from db.DAO import DAO

router = Router()

@router.callback_query(F.data.endswith('top'))
async def check_top(call: CallbackQuery):
    # await DAO.get_top_from_game(call.data[:-4])
    text = await game.get_top(call.data[:-4])
    await call.message.answer(text)
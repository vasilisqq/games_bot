from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from gameControll.game import game

router = Router()
@router.callback_query(F.data == "wordlie_from_friend")
async def game_wordlie_from_friend(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data(state="f_in_game_wordlie")
    await call.message.answer("Введите слово")
    await state.set_state(game.state)

@router.callback_query(F.data == "wordlie_diss")
async def disconnect(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("Вы отклонили запрос на игру")

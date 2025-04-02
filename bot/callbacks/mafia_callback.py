from aiogram import Router, F
from aiogram.types import CallbackQuery
from gameControll.game import game

router = Router()

@router.callback_query(F.data == "join_to_mafia_game")
async def join_to_mafia_room(query: CallbackQuery) -> None:
    ...
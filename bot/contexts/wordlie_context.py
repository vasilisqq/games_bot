from aiogram import Router
from gameControll.game import game
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

router = Router()
@router.message(game.state)
async def step_in_the_game(message: Message, state:FSMContext):
    a:dict[str, str] = await state.get_data()
    if a["state"] == "in_game_wordlie":
        await message.answer("jidhsjk")
    print("sjdkjshkjjskd")
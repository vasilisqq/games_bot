from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from bot.texts import start_text
from bot.config import settings
from gameControll.game import game
from aiogram.fsm.context import FSMContext
from bot.keyboards.reply_keyboard import choose_game_or_else
from bot.logger import cl

router = Router()


@router.message(Command("start"))
async def start_bot(message: Message):
    cl.custom_logger.info(
        "команда старт",
        extra={"username": message.from_user.username,
               "state": "None",
               "handler_name": "start_bot",
               "params":"{}"}
    )
    await message.answer_animation(
        animation=FSInputFile(f"{settings.HOME_PATH}/medias/gifs/start.mp4"),
        caption=start_text,
        reply_markup=choose_game_or_else,
        message_effect_id="5159385139981059251"
    )


@router.message(Command("exit"))
async def exit_all_games(message: Message, state: FSMContext):
    a = await state.get_data()
    if a == {} or not a["state"].startswith("in_game"):
        await message.answer("у тебя нет начатых игр")
        cl.custom_logger.info(
        "пользователь завершил все начатые игры (их не было)",
        extra={"username": message.from_user.username,
               "state": "cleared",
               "handler_name": "exit_all_games",
               "params":"{}"}
    )
        return
    elif a["state"].endswith("wordlie"):
        text, _ = await game.wordlie.del_game_pre(message.from_user.id)
        if _:
            await message.bot.send_message(
                chat_id=_,
                text=f"пользователь @{message.from_user.username} досрочно завершил игру"
            )
    elif a["state"].endswith("cross-zeroes"):
        text = "игра закончится автоматически совсем скоро"
    await message.answer(text)  
    await state.clear()
    cl.custom_logger.info(
        "пользователь завершил все начатые игры",
        extra={"username": message.from_user.username,
               "state": "cleared",
               "handler_name": "exit_all_games",
               "params":"{}"}
    )


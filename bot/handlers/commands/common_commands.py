from aiogram import Router,F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from bot.texts import start_text
from bot.config import settings
from gameControll.game import game
from aiogram.fsm.context import FSMContext
from bot.keyboards.reply_keyboard import choose_game_or_else
from bot.texts import create_user_name
from bot.logger import cl
from bot.keyboards.inline_keyboard import create_join_button
router = Router()


@router.message(Command("start"), F.chat.type == "private")
async def start_bot(message: Message, user):
    args = message.text.split(maxsplit=1)
    
    if len(args) > 1:  # Если есть параметры
        args = args[1].split("_")
        id = args[0]
        name = args[1]
        is_added = await game.add_user_in_mafia_game(id, user)
        text = "нажми на кнопку ниже, чтобы зарегестрироваться на игру\n\n"
        if is_added:
            for item in is_added:
                text += create_user_name(item) + "\n"
            await message.bot.edit_message_text(
            text=text,
            chat_id=id,
            message_id=message.message_id,
            parse_mode="HTML",
            reply_markup=await create_join_button(message.chat.id)
            )
            message.answer(f"ты присоединился в игре в <b>{name}</b>",parse_mode="HTML")
        else:
            await message.answer("ты уже зарегестрирован в игру", show_alert=True)
    else:
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
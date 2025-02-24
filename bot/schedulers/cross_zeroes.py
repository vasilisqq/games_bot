from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ChosenInlineResult
from gameControll.game import game
from bot.keyboards.inline_keyboard import return_to_bot
from bot.bot_configs import set_state
from db.DAO import DAO
from bot.logger import cl
from bot.texts import create_user_name

async def kick_game(query: CallbackQuery|ChosenInlineResult,is_end=False)->None:
    if not is_end:
        await query.bot.edit_message_text(
        text="игра заброшена(",
        inline_message_id=query.inline_message_id,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[return_to_bot]])
        )
    game.crossZeroes.scheduler.remove_job(query.inline_message_id)
    del game.crossZeroes.rooms[query.inline_message_id]
    cl.custom_logger.info(
        f"игра в крестики нолики inline завершена досрочно id: {query.inline_message_id}",
        extra={"username": query.from_user.id,
               "state": "None",
               "handler_name": "kick_game",
               "params":"{}"}
    )

async def kick_open_game(query: CallbackQuery, properties: dict, user, first: bool = False) -> None:
    if first:
        text = (f'игру забросил {create_user_name(user)} \n\n ')
        game.crossZeroes.scheduler.remove_job(str(properties["players"][0].user_id))
        text1 = text + "rang -8"
        await query.bot.edit_message_text(text=text1,
                                        chat_id=properties["first_player"].user_id, 
                                        message_id=properties["message_id"][properties["first_player"].user_id],
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                                            text="заново", callback_data="reload_cross_zeroes_callback"
                                        )]]),
                                        parse_mode="HTML")
        sp = properties["players"][0].user_id if properties["first_player"].user_id == properties["players"][1].user_id else properties["players"][1].user_id
        text2 = text + "rang +8"
        await query.bot.edit_message_text(text=text2,
                                        chat_id=sp, 
                                        message_id=properties["message_id"][sp],
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                                            text="заново", callback_data="reload_cross_zeroes_callback"
                                        )]]),
                                        parse_mode="HTML")        
        await DAO.player_win_and_loose(
                    sp,
                    properties["first_player"].user_id)
    else:
        sp = properties["players"][0] if properties["players"][1].user_id == query.from_user.id else properties["players"][1]
        print(sp.user_id)
        print(query.from_user.id)
        text = (
        f"игру забросил {create_user_name(sp)} \n\n " 
        )
        game.crossZeroes.scheduler.remove_job(query.data[1:])
        print("a")
        await query.bot.edit_message_text(text=text + "rang +8",
                                            chat_id=query.from_user.id, 
                                            message_id=properties["message_id"][query.from_user.id],
                                            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                                            text="заново", callback_data="reload_cross_zeroes_callback"
                                        )]]),
                                        parse_mode="HTML")
        await query.bot.edit_message_text(text=text + "rang -8",
                                            chat_id=sp.user_id, 
                                            message_id=properties["message_id"][sp.user_id],
                                            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                                            text="заново", callback_data="reload_cross_zeroes_callback"
                                        )]]),
                                        parse_mode="HTML")
        await DAO.player_win_and_loose(
                    sp.user_id,
                    query.from_user.id)
    await set_state(query.bot, properties["players"][0].user_id, "")
    await set_state(query.bot, properties["players"][1].user_id, "")
    cl.custom_logger.info(
        "игра в крестики-нолики в боте закончена досрочно",
        extra={"username": [properties["players"][0].user_id,properties["players"][0].user_id],
               "state": "None",
               "handler_name": "kick_open_game",
               "params":"{}"}
    )

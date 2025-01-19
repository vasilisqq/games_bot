from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ChosenInlineResult
from gameControll.game import game
from bot.keyboards.inline_keyboard import return_to_bot
from bot.bot_configs import set_state
from db.DAO import DAO

async def kick_game(query: CallbackQuery|ChosenInlineResult, is_end=False)->None:
    if not is_end:
        await query.bot.edit_message_text(
        text="игра заброшена(",
        inline_message_id=query.inline_message_id,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[return_to_bot]])
        )
    game.crossZeroes.scheduler.remove_job(query.inline_message_id)
    del game.crossZeroes.rooms[query.inline_message_id]

async def kick_open_game(query: CallbackQuery, properties: dict, first: bool = False) -> None:
    if first:
        text = (f"игру забросил @{properties["first_player"][0]} \n\n ")
        game.crossZeroes.scheduler.remove_job(properties["players"][0][0])
        text1 = text + "rang -8"
        await query.bot.edit_message_text(text=text1,
                                        chat_id=properties["first_player"][1], 
                                        message_id=properties["message_id"][properties["first_player"][1]],
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                                            text="заново", callback_data="reload_cross_zeroes_callback"
                                        )]]))
        sp = properties["players"][1 - properties["players"].index(properties["first_player"])][1]
        text2 = text + "rang +8"
        await query.bot.edit_message_text(text=text2,
                                        chat_id=sp, 
                                        message_id=properties["message_id"][sp],
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                                            text="заново", callback_data="reload_cross_zeroes_callback"
                                        )]]))        
        await DAO.player_win_and_loose(
                    sp,
                    properties["first_player"][1])
    else:
        text = (
        f"игру забросил @{properties["players"][1 - properties["players"].index([query.from_user.username, query.from_user.id])][0]} \n\n " 
        )
        game.crossZeroes.scheduler.remove_job(query.data[1:])
        await query.bot.edit_message_text(text=text + "rang +8",
                                            chat_id=query.from_user.id, 
                                            message_id=properties["message_id"][query.from_user.id],
                                            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                                            text="заново", callback_data="reload_cross_zeroes_callback"
                                        )]]))
        sp = properties["players"][1 - properties["players"].index([query.from_user.username, query.from_user.id])][1]
        await query.bot.edit_message_text(text=text + "rang -8",
                                            chat_id=sp, 
                                            message_id=properties["message_id"][sp],
                                            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                                            text="заново", callback_data="reload_cross_zeroes_callback"
                                        )]]))
        await DAO.player_win_and_loose(
                    sp,
                    query.from_user.id)
    await set_state(query.bot, properties["players"][0][1], "")
    await set_state(query.bot, properties["players"][0][0], "")

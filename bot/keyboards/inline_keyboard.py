from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup

def create_cross_aeroes() -> InlineKeyboardMarkup: 
    cross_zeroes_markup = InlineKeyboardBuilder()
    [cross_zeroes_markup.button(text=" ", callback_data=str(i)) for i in range(9)]
    cross_zeroes_markup.adjust(*[3]*3)
    return cross_zeroes_markup.as_markup()


return_to_bot = InlineKeyboardButton(text="к боту", 
                                     url="https://t.me/gamedota22_bot")

choose_game = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="крестики-нолики", callback_data="cross_zeroes")
    ]]
)

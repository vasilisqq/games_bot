from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

choose_game_or_else = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="выбор игры")
    ],[
        KeyboardButton(text="настройки")
    ],[
        KeyboardButton(text="топ игроков")
    ]],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="используй кнопки",
    selective=True
)
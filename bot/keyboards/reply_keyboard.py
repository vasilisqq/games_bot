from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

choose_game_or_else = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="Выбор игры")
    ],[
        KeyboardButton(text="Настройки⚙️")
    ],[
        KeyboardButton(text="Сильнейшие игроки💪")
    ]],
    resize_keyboard=True,
    input_field_placeholder="используй кнопки",
    selective=True
)
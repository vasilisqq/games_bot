from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButtonRequestChat, SwitchInlineQueryChosenChat, CopyTextButton
from aiogram.types import InlineKeyboardMarkup

def create_cross_aeroes(uniq_id:str=None) -> InlineKeyboardMarkup: 
    cross_zeroes_markup = InlineKeyboardBuilder()
    if uniq_id:
        [cross_zeroes_markup.button(text=" ", callback_data=str(i)+uniq_id) for i in range(9)]
    else:
        [cross_zeroes_markup.button(text=" ", callback_data=str(i)) for i in range(9)]    
    cross_zeroes_markup.adjust(*[3]*3)
    return cross_zeroes_markup.as_markup()


return_to_bot = InlineKeyboardButton(text="к боту", 
                                     url="https://t.me/gamedota22_bot")

choose_game = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="крестики-нолики", callback_data="cross-zeroes"),
        InlineKeyboardButton(text="вордли", callback_data="wordlie")
    ]
    ]
)
friend_or_alone = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="Играть с другом💏", switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat(
            allow_user_chats=True
        ))
    ],
    [
        InlineKeyboardButton(text="Играть с другими игроками💫", callback_data="game_alone")
    ]]
)

friend_or_alone_ni = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="Играть с другом💏",callback_data="with_friend")
    ],
    [
        InlineKeyboardButton(text="Играть одному", callback_data="game_alone_")
    ]]
)

show_top = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="крестики-нолики", callback_data="cross-zeroes_top"),
        InlineKeyboardButton(text="вордли", callback_data="wordlie_top")
    ]
    ]
)
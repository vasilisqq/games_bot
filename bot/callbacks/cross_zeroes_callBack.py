from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineQuery
from bot.keyboards.inline_keyboard import create_cross_aeroes

router = Router()

@router.callback_query(F.data.in_([str(i) for i in range(9)]))
async def mark_button(query: CallbackQuery):
    #print(query)
    print("kjssgdddddddddddf")
    #await query.message.answer("djkdshfhkd")
    keyboard = create_cross_aeroes()
    #await query.answer("соси",show_alert=True)
    #print("asjgd")
    #print(query.data)
    #print(keyboard.inline_keyboard[0])
    print(query)
    if(int(query.data) in range(3)):
        keyboard.inline_keyboard[0][int(query.data)].text = "1"
    if(int(query.data) in range(3,6)):
        keyboard.inline_keyboard[1][int(query.data)-3].text = "1"
    if(int(query.data) in range(6,9)):
        keyboard.inline_keyboard[2][int(query.data)-6].text = "1"
    await query.bot.edit_message_reply_markup(inline_message_id=query.inline_message_id, reply_markup=keyboard)
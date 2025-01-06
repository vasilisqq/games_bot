from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.keyboards.inline_keyboard import choose_game
from gameControll.game import game

router = Router()
@router.callback_query(F.data == "game_alone")
async def go_to_cross_zeroes(call: CallbackQuery)-> None:
    await call.message.delete()
    await call.message.answer("Выбери игру", reply_markup=choose_game)

@router.callback_query(F.data == "cross-zeroes")
async def find_opp(call: CallbackQuery) -> None:
    await call.message.delete()
    await call.message.answer("идет поиск противника")
    a = await game.crossZeroes.add_to_listener(call.from_user)
    if a == None:
        await call.message.answer("все еще идет поиск")
    else:
        m = await call.message.answer(text=a[0],
                                       reply_markup=a[1])
        # print(m.message_id)
        # print(call.from_user.id)
        # print(call.message.message_id)
        await call.bot.delete_message(
            chat_id=call.from_user.id,
            message_id=m.message_id
        )
        m1 = await call.bot.send_message(
            chat_id=a[2],
            text=a[0],
            reply_markup=a[1]
        )
        await call.bot.delete_message(
            chat_id=a[2],
            message_id=m1.message_id
        )
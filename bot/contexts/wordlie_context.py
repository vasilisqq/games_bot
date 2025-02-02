from aiogram import Router
from gameControll.game import game
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from gameControll.game import game
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()
@router.message(game.state)
async def step_in_the_game(message: Message, state:FSMContext):
      a:dict[str, str] = await state.get_data()
      if a["state"] == "in_game_wordlie":
            m:str = message.text.lower()
            if not await game.wordlie.check_word_for_russian(m):
                  await message.answer("введи корректное слов, состоящее только из русских букв")
            elif len(m)!=5:
                  await message.answer("введи слово, соостоящее только из 5 букв")
            elif not await game.wordlie.check_word_available(m):
                  await message.answer("я не знаю такого слова попробуй еще раз")
            else:
                  answer, _ = await game.wordlie.check_correct_word(
                  m,
                  message.from_user.id
            )   
                  if _ != None:
                        await message.answer(answer,
                                       reply_markup=InlineKeyboardMarkup(
                                             inline_keyboard=[[InlineKeyboardButton(
                                                   text="сыграть еще раз",
                                                   callback_data="game_alone_"
                                             )]]
                                       ))
                        await state.clear()
                  else:
                        await message.answer(answer)

                  
            
      else:
            await message.answer("я хз как ты сюда попал")

@router.message(game.wordlie.send_word)
async def check_word(message: Message):
      user, word = message.text.split(" ")
      print(await message.bot.get_chat("@"+user))
      await message.bot.send_message(
            chat_id=user,
            text=word
      )



    
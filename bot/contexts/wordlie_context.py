from aiogram import Router
from gameControll.game import game
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.keyboards.reply_keyboard import choose_game_or_else
from gameControll.game import game
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards.inline_keyboard import choose_game

router = Router()
@router.message(game.state)
async def step_in_the_game(message: Message, state:FSMContext):
      print(await state.get_data())
      a:dict[str, str] = await state.get_data()
      if a["state"] in ["in_game_wordlie","f_in_game_wordlie"]:
            m:str = message.text.lower()
            if not await game.wordlie.check_word_for_russian(m):
                  await message.answer("введи корректное слов, состоящее только из русских букв")
            elif len(m)!=5:
                  await message.answer("введи слово, соостоящее только из 5 букв")
            elif not await game.wordlie.check_word_available(m):
                  await message.answer("я не знаю такого слова попробуй еще раз")
            else:
                  if a["state"].startswith("f"):
                        answer, _ = await game.wordlie.check_correct_word(
                        m,
                        message.from_user.id,
                        False
                  )
                  else:
                        answer, _ = await game.wordlie.check_correct_word(
                        m,
                        message.from_user.id
                  )         
                  if _ != None:
                        if answer.endswith('и'):
                              await message.answer(answer)
                              sender = game.wordlie.rooms[message.from_user.id]["sender"]
                              if not sender is None:
                                    if _:
                                          text = (f"😢 Увы, {message.from_user.username} отгадал слово. 😞\n\n"+ 
                                               f"🔤 Слово загаданное: [{game.wordlie[message.from_user.id]["word"]}] 🕵️‍♂️\n\n"+ 
                                                f"Попыток было: 🤯 {game.wordlie[message.from_user.id]["attempts"]}")
                                    else:
                                          text = (f"🎉 Поздравляю! 🎉 {message.from_user.username} не отгадал слово! 🥳\n\n"+
                                                   f"🔤 Слово загаданное: [{game.wordlie[message.from_user.id]["word"]}]🕵️‍♂️")
                                    await message.bot.send_message(
                                           chat_id=sender,
                                           text=text     
                                          )

                        else:
                              await message.answer(answer,
                                          reply_markup=InlineKeyboardMarkup(
                                                inline_keyboard=[[InlineKeyboardButton(
                                                      text="сыграть еще раз",
                                                      callback_data="game_alone_"
                                                )]]
                                          ))
                        await state.clear()
                        del game.wordlie.rooms[message.from_user.id]
                  else:
                        await message.answer(answer)

                  
            
      else:
            await message.answer("я хз как ты сюда попал")

@router.message(game.wordlie.send_word)
async def check_word(message: Message, state: FSMContext):
      if message.text == "отмена":
            await state.clear()
            #await message.delete()
            await message.answer("действие отменено",
            reply_markup=choose_game_or_else)
            await message.delete()
            await message.answer("Выбери игру, в которую хочешь поиграть",
                       reply_markup=choose_game)
            return       
      try:
            user, word = message.text.split(" ")
      except:
            await message.answer("введи корректное сообщение")
      else:
            if user == message.from_user.username:
                  await message.answer("нельзя загадать слово самому себе")
            else:
                  users = await game.wordlie.get_user_by_name(user)
                  await game.wordlie.create_alone_game(users, word, message.from_user.id)
                  try:
                        await message.bot.send_message(
                        chat_id=users,
                        text=f"{message.from_user.username} бросил тебе вызов в wordle",
                        reply_markup=InlineKeyboardMarkup(
                              inline_keyboard=[[
                                    InlineKeyboardButton(text="пройти", callback_data="wordlie_from_friend"),
                                    InlineKeyboardButton(text="отказаться", callback_data="wordlie_diss")
                              ]]
                        )
                  )
                  except:
                        await message.answer("пользователь должен иметь чат с ботом, чтобы бы отправил ему вызов")
                  else:
                        await message.answer(f"приглашение отправлено игроку @{user}", reply_markup=choose_game_or_else)
                        await state.clear()


    
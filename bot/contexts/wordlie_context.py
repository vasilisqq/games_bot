from aiogram import Router
from gameControll.game import game
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.keyboards.reply_keyboard import choose_game_or_else
from gameControll.game import game
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards.inline_keyboard import choose_game
from bot.logger import cl
from bot.texts import create_user_name

router = Router()
@router.message(game.state)
async def step_in_the_game(message: Message, state:FSMContext):
      a:dict[str, str] = await state.get_data()
      if a["state"] in ["in_game_wordlie", "f_in_game_wordlie"]:
            m:str = message.text.lower()
            if not await game.wordlie.check_word_for_russian(m):
                  await message.answer("введи корректное слов, состоящее только из русских букв")
                  cl.custom_logger.info(
                    f"пользователь в вордли ввел слово не из русских букв",
                        extra={"username": message.from_user.username,
                        "state": await state.get_data(),
                        "handler_name": "step_in_the_game",
                        "params":{"word": m}}
                        )
            elif len(m)!=5:
                  await message.answer("введи слово, соостоящее только из 5 букв")
                  cl.custom_logger.info(
                    f"пользователь в вордли ввел слово длиннее 5 букв",
                        extra={"username": message.from_user.username,
                        "state": await state.get_data(),
                        "handler_name": "step_in_the_game",
                        "params":{"word": m}}
                        )
            elif not await game.wordlie.check_word_available(m):
                  await message.answer("я не знаю такого слова попробуй еще раз")
                  cl.custom_logger.info(
                    f"пользователь в вордли ввел несуществующее слово",
                        extra={"username": message.from_user.username,
                        "state": await state.get_data(),
                        "handler_name": "step_in_the_game",
                        "params":{"word": m}}
                        )
            else:
                  answer, _ = await game.wordlie.check_correct_word(
                        m,
                        message.from_user.id,
                        not a["state"].startswith("f")
                  )         
                  if _ != None:
                        if a["state"].startswith("f"):
                              await message.answer(answer)
                              sender = game.wordlie.rooms[message.from_user.id]["sender"]
                              if _:
                                    text = (f"😢 Увы, @{message.from_user.username} отгадал слово. 😞\n\n"+ 
                                         f"🔤 Слово загаданное: [{game.wordlie.rooms[message.from_user.id]["word"]}] 🕵️‍♂️\n\n"+ 
                                          f"Попыток было: 🤯 {game.wordlie.rooms[message.from_user.id]["attempts"]}")
                                    cl.custom_logger.info(
                                          f"пользователь отгадал слово от друга",
                                          extra={"username": message.from_user.username,
                                          "state": await state.get_data(),
                                          "handler_name": "step_in_the_game",
                                          "params":{"word": answer}}
                                    )
                              else:
                                    text = (f"🎉 Поздравляю! 🎉 @{message.from_user.username} не отгадал слово! 🥳\n\n"+
                                                f"🔤 Слово загаданное: [{game.wordlie.rooms[message.from_user.id]["word"]}]🕵️‍♂️")
                                    cl.custom_logger.info(
                                          f"пользователь не отгадал слово от друга",
                                          extra={"username": message.from_user.username,
                                          "state": await state.get_data(),
                                          "handler_name": "step_in_the_game",
                                          "params":{"word": answer}}
                                    )
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
                              cl.custom_logger.info(
                                          f"пользователь закончил игру в вордли",
                                          extra={"username": message.from_user.username,
                                          "state": await state.get_data(),
                                          "handler_name": "step_in_the_game",
                                          "params":{"word": answer}}
                                    )
                        await state.clear()
                        del game.wordlie.rooms[message.from_user.id]
                  else:
                        await message.answer(answer)
                        cl.custom_logger.info(
                                          f"пользователь совершил попытку отгадать слово",
                                          extra={"username": message.from_user.username,
                                          "state": await state.get_data(),
                                          "handler_name": "game_wordlie_from_friend",
                                          "params":{"word": answer}}
                                    )

                  
            
      else:
            await message.answer("я хз как ты сюда попал")

@router.message(game.wordlie.send_word)
async def check_word(message: Message, state: FSMContext,user):
      if message.text == "отмена":
            await state.clear()
            await message.answer("действие отменено",
            reply_markup=choose_game_or_else)
            await message.delete()
            await message.answer("Выбери игру, в которую хочешь поиграть",
                       reply_markup=choose_game)
            return       
      try:
            userr, word = message.text.split(" ")
      except:
            await message.answer("введи корректное сообщение")
      else:
            if userr == message.from_user.username:
                  await message.answer("нельзя загадать слово самому себе")
            else:
                  users = await game.wordlie.get_user_by_name(userr)
                  print(users)
                  # print(await message.bot.get_chat(f"@{message.from_user.username}"))
                  await game.wordlie.create_alone_game(users, word, message.from_user.id)
                  try:
                        await message.bot.send_message(
                        chat_id=users,
                        text=f"{create_user_name(user)} бросил тебе вызов в wordle",
                        reply_markup=InlineKeyboardMarkup(
                              inline_keyboard=[[
                                    InlineKeyboardButton(text="пройти", callback_data="wordlie_from_friend"),
                                    InlineKeyboardButton(text="отказаться", callback_data="wordlie_diss")
                              ]]
                        ),
                        parse_mode="HTML"
                  )
                  except:
                        await message.answer("пользователь должен иметь чат с ботом, чтобы бы отправил ему вызов")
                  else:
                        await message.answer(f"приглашение отправлено игроку @{userr}", reply_markup=choose_game_or_else)
                        await state.clear()

    
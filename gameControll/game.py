from gameControll.crossZeroes import CrossZeroes
from gameControll.wordlie import Wordlie
from gameControll.mafiaControll import Mafia
from aiogram.fsm.state import State, StatesGroup
from db.DAO import DAO
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from typing import Union
from aiogram import Bot

class Game(StatesGroup):
    crossZeroes = CrossZeroes()
    wordlie = Wordlie()
    mafia_games : dict[Union[str|int], Mafia] = {}
    state = State()
    mafia_schedule = AsyncIOScheduler(timezone="Europe/Moscow")

    async def get_top(self, game_name):
        top = await DAO.get_top_from_game(game_name)
        text = (
            f"🥇 @{top[0].username} {top[0].rait} \n"+
            f"🥈 @{top[1].username} {top[1].rait} \n"+
            f"🥉 @{top[2].username} {top[2].rait} \n"+
            f"   @{top[3].username} {top[3].rait} \n"+
            f"   @{top[4].username} {top[4].rait} \n"
        )
        return text

    async def create_mafia_game(self, key:int|str, callable: int|str, bot, m):
        self.mafia_games.update({key: Mafia(callable,m)})
        self.mafia_schedule.add_job(
            self.start_or_not,
            trigger='interval',
            minutes = 2,
            kwargs={'bot':bot, 'id_game': key},
            id= str(key)
        )

    async def start_or_not(self, bot: Bot, id_game):
        if len(self.mafia_games[id_game].players) < 4:
            await bot.delete_message(
                chat_id=id_game,
                message_id=self.mafia_games[id_game].last_message
            )
            del self.mafia_games[id_game]
            await bot.send_message(
                text="Недостаточное количестве игроков",
                chat_id=id_game)
        else:
            ...
        self.mafia_schedule.remove_job(str(id_game))



game = Game()

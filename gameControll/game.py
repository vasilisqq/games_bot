from gameControll.crossZeroes import CrossZeroes
from gameControll.wordlie import Wordlie
from gameControll.mafiaControll import Mafia
from aiogram.fsm.state import State, StatesGroup
from db.DAO import DAO
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class Game(StatesGroup):
    crossZeroes = CrossZeroes()
    wordlie = Wordlie()
    mafia_games : dict[str, Mafia]
    state = State()


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

    async def create_mafia_game(self, key:int, callable: int|str):
        self.mafia_games.update({key: Mafia(callable)})


game = Game()

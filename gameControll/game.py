from gameControll.crossZeroes import CrossZeroes
from gameControll.wordlie import Wordlie
from aiogram.fsm.state import State, StatesGroup

class Game(StatesGroup):
    crossZeroes = CrossZeroes()
    wordlie = Wordlie()
    state = State()
game = Game()

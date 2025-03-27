from typing import Union

class Mafia:
    players: Union[str|int]
    async def __init__(self, callable: str|int) -> None:
        self.players.append(callable)    
    async def create_game(self, key:int):
        self.game.update({key:{}})
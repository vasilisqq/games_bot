from typing import Union
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class Mafia:
    players: list[Union[str|int]] = []
    last_message: str|int

    def __init__(self, callable: str|int,m) -> None:
        self.players.append(callable)
        self.last_message = m
    
    async def add_user(self, id):
        if not id in self.players:
            self.players.append(id)
            return self.players     
        return None
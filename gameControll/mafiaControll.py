from typing import Union
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class Mafia:
    players = []
    last_message: str|int

    def __init__(self, callable: str|int,m) -> None:
        self.players.append(callable)
        self.last_message = m
    
    async def add_user(self, user):
        for item in self.players:
            if user.user_id == item.user_id:
                return None
        self.players.append(user)     
        return self.players
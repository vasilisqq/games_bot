from typing import Union
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import random

MAFIA_ROLES = ["Дон", "Доктор", "Мирный житель"]

class Mafia:
    players = []
    last_message: str|int
    civilian = []
    don = None
    doctor = None

    def __init__(self, callable: str|int,m) -> None:
        self.players.append(callable)
        self.last_message = m
    
    async def add_user(self, user):
        for item in self.players:
            if user.user_id == item.user_id:
                return None
        self.players.append(user)     
        return self.players
    
    async def start_game(self):
        match len(self.players):
            case 4:
                self.don = random.choice(self.players)
                self.players.remove(self.don)
                self.doctor = random.choice(self.players)
                self.players.remove(self.doctor)
                self.civilian = self.players.copy()
            case _:
                ...

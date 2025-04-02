from typing import Union
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class Mafia:
    players: list[Union[str|int]]

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    async def __init__(self, callable: str|int) -> None:
        self.players.append(callable)

    async def registration_schedule(self):
        if len(self.players) < 4:
            ...

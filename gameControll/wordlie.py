import random

class Wordlie:
    rooms = {}
    words: list[str] = []
    async def create_alone_game(self, user_id: int|str):
        self.rooms.update({user_id: random.choice(self.words),
                           "attempts": 0})

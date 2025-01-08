from db.database import async_session_maker
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import update
from db.models.user import Users
import asyncio

class DAO:
    @classmethod
    async def create_and_return_user(cls, user_id:int):
        async with async_session_maker() as session:
            user = insert(Users).values(user_id=user_id)
            user = user.on_conflict_do_nothing().returning(Users)
            res = await session.execute(user)
            await session.commit()
            return res.scalar_one_or_none()
    @classmethod
    async def player_win_and_loose(cls, user_id1:int, user_id2: int) -> None:
        async with async_session_maker() as session:
            user = update(Users).where(Users.user_id == user_id1).values(
                raiting_cross_zeroes=Users.raiting_cross_zeroes+8)
            await session.execute(user)
            user = update(Users).where(Users.user_id == user_id2).values(
                raiting_cross_zeroes=Users.raiting_cross_zeroes-8)
            await session.execute(user)
            await session.commit()


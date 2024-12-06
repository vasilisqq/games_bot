from db.database import async_session_maker
from sqlalchemy.dialects.postgresql import insert
from db.models.user import Users
import asyncio

class DAO:
    @classmethod
    async def create_and_return_user(cls, user_id):
        async with async_session_maker() as session:
            user = insert(Users).values(user_id=user_id)
            user = user.on_conflict_do_nothing().returning(Users)
            res = await session.execute(user)
            return res.scalar_one_or_none()


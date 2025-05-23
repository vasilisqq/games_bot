from db.database import async_session_maker
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import update, select, or_, case, func
from db.models.user import Users
from bot.logger import cl

class DAO:


    @classmethod
    async def create_and_return_user(cls, user_id:int, username, name):
        async with async_session_maker() as session:
            user = insert(Users).values(user_id=user_id, username=username, name=name)
            user = user.on_conflict_do_update(
                index_elements=["user_id"],
                set_={"username":username, "name":name}
            ).returning(Users)
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
                raiting_cross_zeroes=func.greatest(0, Users.raiting_cross_zeroes-8))
            await session.execute(user)
            await session.commit()
            cl.custom_logger.info(
        "у пользователей изменен рейтинг в крестики-нолики",
        extra={"username": [user_id1, user_id2],
               "state": "None",
               "handler_name": "player_win_and_loose",
               "params": {}}
    )

    @classmethod
    async def get_two_raiting(cls, user_id1:int, user_id2: int) -> list[int]:
        async with async_session_maker() as session:
            query = select(Users.raiting_cross_zeroes).where(
                or_(Users.user_id == user_id1, Users.user_id == user_id2)
            )
            answer = await session.execute(query)
            return [item for item in answer.scalars()]
            

    @classmethod
    async def wordlie_change_rait(cls, user_id, rait):
        async with async_session_maker() as session:
            user = update(Users).where(Users.user_id == user_id).values(
                raiting_wordlie=func.greatest(0, Users.raiting_wordlie+rait))
            await session.execute(user)
            await session.commit()
            cl.custom_logger.info(
        "у пользователя изменен рейтинг wordlie",
        extra={"username": user_id,
               "state": "None",
               "handler_name": "wordlie_change_rait",
               "params": {}}
    )

    
    @classmethod
    async def get_user_id_by_username(cls, username:str):
        async with async_session_maker() as session:
            query = select(Users.user_id).where(Users.name==username)
            user = await session.execute(query)
            return user.scalar_one_or_none()

    @classmethod
    async def get_top_from_game(cls, game:str):
        async with async_session_maker() as session:
            if game == "cross-zeroes":
                query = select(
                    Users.username, 
                    Users.raiting_cross_zeroes.label("rait")).order_by(
                        Users.raiting_cross_zeroes.desc()
                    ).limit(5)
            elif game == "wordlie":
                query = select(
                    Users.username, 
                    Users.raiting_wordlie.label("rait")).order_by(
                        Users.raiting_wordlie.desc()
                    ).limit(5)
            users = await session.execute(query)
            return users.all()



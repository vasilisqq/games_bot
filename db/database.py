from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import asyncpg

DB_HOST = "localhost" 
DB_PORT = 5432
DB_USER = "postgres"
DB_PASS = "1234"
DB_NAME = "games_db"

# Ссылка на базу данных
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# создаем движок для передачи ссылки в базы данных в sqlalchemy(создание движка)
engine = create_async_engine(DATABASE_URL)

# генератор сессий (транзакций)   (движок         класс, который будем ждать     при завершении транзакции не отключаться от базы данных) 
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# класс, который используется для миграций
class Base(DeclarativeBase):
    pass
from db.database import Base
from sqlalchemy import Column, BigInteger, Integer

class Users(Base):
    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True, autoincrement=False)
    raiting_cross_zeroes = Column(Integer, default=0, nullable=False)
    
from db.database import Base
from sqlalchemy import Column, BigInteger, Integer, String, CheckConstraint

class Users(Base):
    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True, autoincrement=False)
    username = Column(String, nullable=False)
    raiting_cross_zeroes = Column(Integer, default=0, nullable=False)
    raiting_wordlie= Column(Integer, default=0, nullable=False)

    __table_args__=(
        CheckConstraint("raiting_cross_zeroes >= 0", name="cross_zeroes_non_negative"),
        CheckConstraint("raiting_wordlie >= 0", name="wordlie_non_negative")
    )
    
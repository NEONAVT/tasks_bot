from datetime import date
from typing import Optional

from sqlalchemy import Integer, String, Date, BigInteger
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.database import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_updated_date: Mapped[date] = mapped_column(Date, nullable=True)
    last_updated_message: Mapped[str] = mapped_column(String, nullable=True)


    def __repr__(self):
        return f"<User(user_id={self.user_id}, chat_id={self.chat_id}, username='{self.username}')>"
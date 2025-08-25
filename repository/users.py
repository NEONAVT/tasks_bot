from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple, Union

from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session
from models import User


@dataclass
class UsersRepository:
    """
    Репозиторий для работы с пользователями в базе данных.

    Атрибуты:
        db_session (Session): SQLAlchemy сессия для работы с базой данных.
    """
    db_session: Session

    def register_user(self, user_id: int, chat_id: int, username: str) -> Optional[User]:
        """
        Регистрирует нового пользователя в базе данных или возвращает существующего.

        Args:
            user_id (int): Идентификатор пользователя.
            chat_id (int): Идентификатор чата пользователя.
            username (str): Имя пользователя.

        Returns:
            User | None: Созданный или найденный пользователь, если успешен,
                         иначе None.
        """
        user = self.get_user(user_id)
        if user:
            return user

        query = insert(User).values(
            user_id=user_id,
            chat_id=chat_id,
            username=username
        ).returning(User.user_id)

        user_id_result: int = self.db_session.execute(query).scalar()
        query_select = select(User).where(User.user_id == user_id_result)
        user = self.db_session.execute(query_select).scalar_one_or_none()
        self.db_session.commit()
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        """
        Получает пользователя по его идентификатору.

        Args:
            user_id (int): Идентификатор пользователя.

        Returns:
            User | None: Пользователь, если найден, иначе None.
        """
        query = select(User).where(User.user_id == user_id)
        return self.db_session.execute(query).scalar_one_or_none()

    def update_last_message_data(
            self,
            user_id: int,
            updated_date: datetime,
            last_message: str
    ) -> Tuple[int, str, str]:
        """
        Обновляет дату последнего сообщения и текст последнего сообщения пользователя.

        Args:
            user_id (int): Идентификатор пользователя.
            updated_date (datetime): Дата и время последнего сообщения.
            last_message (str): Текст последнего сообщения.

        Returns:
            Tuple[int, str, str]: Кортеж (user_id, username, last_message) после обновления.

        Raises:
            ValueError: Если пользователь с указанным user_id не найден.
            RuntimeError: Если обновление в базе данных не удалось.
        """
        user = self.get_user(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")

        query = (
            update(User)
            .where(User.user_id == user_id)
            .values(
                last_updated_date=updated_date,
                last_updated_message=last_message
            )
            .returning(User.user_id, User.username, User.last_updated_message)
        )
        result: Optional[Tuple[int, str, str]] = self.db_session.execute(query).one_or_none()
        if not result:
            raise RuntimeError("Failed to update date in DB")
        self.db_session.commit()
        return result

from dataclasses import dataclass
from database import SessionFactory
from repository import UsersRepository
import logging

logger = logging.getLogger(__name__)

@dataclass
class UsersService:

    def register_user(self, user_id: int, chat_id: int, username: str):
        try:
            with SessionFactory() as session:
                repo = UsersRepository(db_session=session)
                user = repo.register_user(user_id, chat_id, username)
                logger.info(f"Пользователь {username} зарегистрирован с ID {user_id}")
                return user
        except Exception as e:
            logger.error(f"Ошибка регистрации пользователя: {e}")
            return None

    def update_last_message_data(self, user_id, updated_date, last_message):
        with SessionFactory() as session:
            repo = UsersRepository(db_session=session)
            return repo.update_last_message_data(user_id, updated_date, last_message)


users_service = UsersService()



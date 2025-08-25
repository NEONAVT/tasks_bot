import logging
from dataclasses import dataclass
from typing import List

from bot import TelegramClient, telegram_client
from database import SessionFactory
from log_config.logging_config import setup_logging
from repository.reminder import ReminderRepository

logger = logging.getLogger(__name__)


@dataclass
class ReminderService:
    telegram_client: TelegramClient

    def execute(self) -> None:
        chat_ids = self.get_inactive_chat_ids()
        if not chat_ids:
            logger.info("Нет неактивных пользователей — напоминания не требуются.")
            return
        logger.info(f"Отправляем напоминание {len(chat_ids)} пользователям: {chat_ids}")
        self.send_reminders(chat_ids)

    # def execute(self) -> None:
    #     """Основной метод: получает chat_id неактивных пользователей и отправляет им напоминание."""
    #     try:
    #         chat_ids = self.get_inactive_chat_ids()
    #         if not chat_ids:
    #             logger.info("Нет неактивных пользователей — напоминания не требуются.")
    #             return
    #
    #         logger.info(f"Отправляем напоминание {len(chat_ids)} пользователям: {chat_ids}")
    #         self.send_reminders(chat_ids)
    #     except Exception as e:
    #         logger.error("Ошибка при выполнении напоминания", exc_info=True)
    #         raise

    def get_inactive_chat_ids(self) -> List[int]:
        """Получает список chat_id пользователей, которые не делали standup сегодня."""
        with SessionFactory() as session:
            repo = ReminderRepository(db_session=session)
            chat_ids = repo.get_chat_ids()
            logger.info(f"Найдено неактивных пользователей: {len(chat_ids)}"
                        f"Неактивные chat_id: {chat_ids}")
            return chat_ids

    def send_reminders(self, chat_ids: List[int]) -> None:
        """Отправляет напоминание каждому пользователю."""
        message = "Как на счет постендапиться сегодня? 😊"
        for chat_id in chat_ids:
            try:
                response = self.telegram_client.post(
                    method="/sendMessage",
                    params={
                        "chat_id": chat_id,
                        "text": message
                    }
                )
                logger.info(f"Напоминание отправлено пользователю {chat_id}. Ответ Telegram: {response}")
            except Exception as e:
                logger.error(f"Не удалось отправить напоминание пользователю {chat_id}", exc_info=True)


if __name__ == "__main__":
    from log_config.logging_config import setup_logging  # путь к твоему модулю

    setup_logging()  # подключаем обработчики

    reminder = ReminderService(telegram_client=telegram_client)
    reminder.execute()

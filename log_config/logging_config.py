import logging
import os
from logging.handlers import RotatingFileHandler
from bot import settings


def setup_logging():
    """
    Настраивает логирование приложения.

    Устанавливает уровень логов из
    settings.LOG_LEVEL. Добавляет консольный и файловый обработчики с
    форматированием из settings.LOG_FORMAT. Файловый обработчик с ротацией:
    размер файла до 100 МБ, 5 резервных копий.
    """
    log_dir = os.path.join(settings.base_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)

    formatter = logging.Formatter(settings.LOG_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        f'{log_dir}/app.log',
        maxBytes=100 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

from bot.settings import settings
from bot.telegram_client import MyBot, telegram_client

bot = MyBot(token=settings.bot_token, telegram_client=telegram_client)
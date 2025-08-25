from datetime import datetime
import requests
import telebot
from bot import settings


class TelegramClient:
    def __init__(self, token: str, admin_chat_id: str, base_url: str = "https://api.telegram.org"):
        self.token = token
        self.admin_chat_id = admin_chat_id
        self.base_url = base_url


    def prepare_url(self, method: str):
        result_url = f"{self.base_url}/bot{self.token}"
        if method is not None:
            result_url += method
        return result_url


    def post(self, method: str = None, params: dict = None,  body = None, timeout=(10, 30)):
        url = self.prepare_url(method)
        try:
            resp = requests.post(url, params=params, data=body, timeout=timeout)
            return resp.json()
        except requests.exceptions.ReadTimeout:
            print(f"ReadTimeout при вызове {method}")
            raise
        except requests.exceptions.ConnectionError as e:
            print(f"ConnectionError при вызове {method}: {e}")
            raise


    def create_err_message(self, err):
        return f"{datetime.now()} :: {err.__class__} :: {err}"


class MyBot(telebot.TeleBot):
    def __init__(self, telegram_client: TelegramClient, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.telegram_client = telegram_client


telegram_client = TelegramClient(
    token=settings.bot_token,
    admin_chat_id=settings.admin_chat_id,
    base_url="https://api.telegram.org")
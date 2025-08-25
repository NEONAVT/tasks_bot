from datetime import date
from telebot.types import Message

from bot import settings


class StandupHandler:
    def __init__(self, bot, users_service):
        self.bot = bot
        self.users_service = users_service
        self.register_handlers()

    @staticmethod
    def handle_standup_speech(message: Message, users_service, bot):
        try:
            update_data = users_service.update_last_message_data(
                user_id=message.from_user.id,
                updated_date=date.today(),
                last_message=message.text
            )
            user_id, username, last_message = update_data
            bot.send_message(settings.admin_chat_id, f"Пользователь {username}(ID: {user_id}) говорит: {last_message}")
            bot.reply_to(message, text="Спасибо большое! Желаю успехов и хорошего дня!")
        except Exception as e:
            print(f"Error in handle_standup_speech: {e}")
            bot.telegram_client.post(
                method="sendMessage",
                params={"text": bot.telegram_client.create_err_message(e)}
            )

    def register_handlers(self):
        @self.bot.message_handler(commands=["say_standup_speech"])
        def say_standup_speech(message: Message):
            sent_message = self.bot.reply_to(
                message,
                text="Привет! Чем ты занимался вчера?\nЧто будешь делать сегодня?\nКакие есть трудности?"
            )
            self.bot.register_next_step_handler(
                sent_message,
                StandupHandler.handle_standup_speech,
                self.users_service,
                self.bot
            )




from telebot.types import Message


def register_start(bot, users_service):
    @bot.message_handler(commands=["start"])
    def start(message: Message):
        print("Команда /start получена")
        try:
            user_id = message.from_user.id
            chat_id = message.chat.id
            username = message.from_user.username

            new_user = users_service.register_user(user_id, chat_id, username)

            if new_user:
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f"Привет, {message.from_user.first_name}! Вы зарегистрированы: {message.from_user.username}! "
                         f"Ваш user_id: {message.from_user.id}")
        except Exception as e:
                bot.telegram_client.post(
                    method="sendMessage",
                    params={"text": bot.telegram_client.create_err_message(e)})

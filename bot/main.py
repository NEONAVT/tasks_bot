from bot.bot_instance import bot
from handlers import register_start, StandupHandler
from log_config.logging_config import setup_logging
from services import users_service
setup_logging()


def main():
    register_start(bot, users_service)
    StandupHandler(bot, users_service)

    try:
        bot.polling(none_stop=True, interval=1)
    except Exception as e:
            bot.telegram_client.post(
                method="sendMessage",
                params={"text": bot.telegram_client.create_err_message(e)})



if __name__ == "__main__":
    main()

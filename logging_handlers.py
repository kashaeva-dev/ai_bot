import logging
import telegram


class BotHandler(logging.Handler):
    def __init__(self, tg_bot_logger_token, tg_chat_id):
        super().__init__()
        self.tg_bot_logger_token = tg_bot_logger_token
        self.tg_chat_id = tg_chat_id

    def emit(self, record):
        bot = telegram.Bot(token=self.tg_bot_logger_token)
        log_entry = self.format(record)
        bot.send_message(chat_id=self.tg_chat_id,
                         text=fr'{log_entry}',
                         )

import logging

from environs import Env

from bots.tg_bot import start_tg_bot
from bots.vk_bot import start_vk_bot
from logging_handlers import BotHandler

logger = logging.getLogger(__name__)

def main():
    env = Env()
    env.read_env()

    TG_BOT_LOGGER_TOKEN = env('TG_BOT_LOGGER_TOKEN')
    TG_CHAT_ID = env('TG_CHAT_ID')

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    logger.addHandler(BotHandler(TG_BOT_LOGGER_TOKEN, TG_CHAT_ID))

    try:
        TG_BOT_TOKEN = env('TG_BOT_TOKEN')
        VK_API_TOKEN = env('VK_API_TOKEN')
        start_tg_bot(TG_BOT_TOKEN, logger)
        start_vk_bot(VK_API_TOKEN, logger)
    except Exception as error:
        logger.exception(error)


if __name__ == '__main__':
    main()

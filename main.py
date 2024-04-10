import argparse
import logging

from environs import Env

from bots.tg_bot import start_tg_bot
from bots.vk_bot import start_vk_bot
from logging_handlers import BotHandler

logger = logging.getLogger(__name__)


def create_parser():
    parser = argparse.ArgumentParser(
        prog="Start telegram and vk bots based on DialogFlow",
    )
    parser.add_argument('--only_tg',
                        action='store_true',
                        help='Start only tg bot',
                        )
    parser.add_argument('--only_vk',
                        action='store_true',
                        help='Start only vk bot',
                        )

    return parser


def main():
    env = Env()
    env.read_env()

    tg_bot_logger_token = env('TG_BOT_LOGGER_TOKEN')
    tg_chat_id = env('TG_CHAT_ID')

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
    )
    logger.addHandler(BotHandler(tg_bot_logger_token, tg_chat_id))

    parser = create_parser()
    args = parser.parse_args()
    try:
        tg_bot_token = env('TG_BOT_TOKEN')
        vk_api_token = env('VK_API_TOKEN')
        df_project_id = env('DF_PROJECT_ID')
        if args.only_tg:
            start_tg_bot(tg_bot_token, logger, df_project_id)
        elif args.only_vk:
            start_vk_bot(vk_api_token, logger, df_project_id)
        else:
            start_tg_bot(tg_bot_token, logger, df_project_id)
            start_tg_bot(tg_bot_token, logger, df_project_id)
    except Exception as error:
        logger.exception(error)


if __name__ == '__main__':
    main()

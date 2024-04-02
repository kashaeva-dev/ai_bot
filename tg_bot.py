import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext
from telegram import Update
from environs import Env
from dialog_flow import get_df_answer


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

env = Env()
env.read_env()

updater = Updater(token=env('TG_BOT_TOKEN'), use_context=True)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте!")

def echo(update: Update, context: CallbackContext):
    df_response = get_df_answer('ai-devman-bot',
                              update.effective_chat.id,
                              text=update.message.text,
                              language_code='ru')
    context.bot.send_message(chat_id=update.effective_chat.id, text=df_response.fulfillment_text)

start_handler = CommandHandler('start', start)
message_handler = MessageHandler(Filters.text & (~Filters.command), echo)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()

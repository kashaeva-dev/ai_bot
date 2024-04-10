from functools import partial

from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext

from dialog_flow.dialog_flow import get_df_answer


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте!")


def answer(df_project_id, update: Update, context: CallbackContext):
    df_response = get_df_answer(df_project_id,
                                update.effective_chat.id,
                                text=update.message.text,
                                language_code='ru')
    context.bot.send_message(chat_id=update.effective_chat.id, text=df_response.fulfillment_text)


def start_tg_bot(token, logger, df_project_id):
    logger.info('Start telegram bot')
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(Filters.text & (~Filters.command), partial(answer, df_project_id))

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_handler)

    updater.start_polling()

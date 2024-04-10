import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from dialog_flow.dialog_flow import get_df_answer


def answer(event, vk_session_api, df_project_id):
    df_query_result = get_df_answer(df_project_id,
                                    event.user_id,
                                    text=event.text,
                                    language_code='ru')
    if not df_query_result.intent.is_fallback:
        vk_session_api.messages.send(
            user_id=event.user_id,
            message=df_query_result.fulfillment_text,
            random_id=random.randint(1, 1000),
        )


def start_vk_bot(token, logger, df_project_id):
    logger.info('Start vk bot')
    vk_session = vk_api.VkApi(token=token)

    longpoll = VkLongPoll(vk_session)

    vk_session_api = vk_session.get_api()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer(event, vk_session_api, df_project_id)

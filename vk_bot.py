import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env
from dialog_flow import get_df_answer


def echo(event, vk_session_api):
    answer = get_df_answer('ai-devman-bot',
                           event.user_id,
                           text=event.text,
                           language_code='ru')
    vk_session_api.messages.send(
        user_id=event.user_id,
        message=answer,
        random_id=random.randint(1,1000)
    )


if __name__ == "__main__":
    env = Env()
    env.read_env()

    vk_session = vk_api.VkApi(token=env('VK_API_TOKEN'))

    longpoll = VkLongPoll(vk_session)

    vk_session_api = vk_session.get_api()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_session_api)

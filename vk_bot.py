import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env


def echo(event, vk_session_api):
    vk_session_api.messages.send(
        user_id=event.user_id,
        message=event.text,
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

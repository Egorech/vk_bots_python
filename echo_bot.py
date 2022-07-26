# import all the libraries for the vk_api
import vk_api
from vk_api.longpoll import VkLongPoll , VkEventType

# libraries with vk token and vk group_id
import  _token

# necessary global variables for the chatbot
group_id = _token.group_id
token = _token.token


def main():
    """
    function that repeats the message
    """

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            vk.messages.send(
                chat_id = event.chat_id ,
                message = event.text
                , random_id = 0
            )


if __name__ == '__main__':

    # linking to vk
    vk_session = vk_api.VkApi(token = token)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    main()

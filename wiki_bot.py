# import all the libraries for the vk_api
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

# import all the libraries for the wiki
import wikipedia

# libraries with vk token and vk group_id
import _token

# necessary global variables for the chatbot
group_id = _token.group_id
token = _token.token


def send_photo(photo1):
    """
    function to send photos
    """

    global attachment
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages(photo1)
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'


def main():
    """
    the main function for the wikipedia query
    """

    wikipedia.set_lang("RU")
    vars = ['википедия', 'вики', 'wikipedia', 'wiki']

    # greeting after sending any message
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            vk.messages.send(
                chat_id = event.chat_id,
                message = "Если хотите узнать что-то, то напишите одну из следующих строк: википедия , вики , wikipedia , wiki",
                random_id = 0
            )
            send_photo('images/img_1.png')
            vk.messages.send(
                chat_id = event.chat_id,
                random_id = 0,
                attachment = attachment
            )
            break

    # enter one of the required strings in the vars variable
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            if (event.text.lower()) in vars:
                vk.messages.send(
                    chat_id = event.chat_id,
                    message = 'Введите запрос:',
                    random_id = 0
                )
                break
            else:
                vk.messages.send(
                    chat_id = event.chat_id,
                    message = "Иди работай, сука",
                    random_id = 0
                )
                send_photo('images/img.png')
                vk.messages.send(
                    chat_id = event.chat_id,
                    random_id = 0,
                    attachment = attachment
                )
                vk.messages.send(
                    chat_id = event.chat_id,
                    message = "Для корректной работы мне нужна одна из этих строк: википедия , вики , wikipedia , wiki",
                    random_id = 0
                )

    # outputting information from wikipedia
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            try:
                vk.messages.send(
                    chat_id = event.chat_id,
                    message = 'Информация по запросу:' + ' ' + event.text + '\n' + str(
                        wikipedia.summary(event.text + ' это')),
                    random_id = 0
                )
                send_photo('images/umnyy-negr_140355423_orig_.jpg')
                vk.messages.send(
                    chat_id = event.chat_id,
                    random_id = 0,
                    attachment = attachment
                )
                vk.messages.send(
                    chat_id = event.chat_id,
                    message = "Если хочешь узнать что-то еще, только спроси !!!",
                    random_id = 0
                )
            except wikipedia.exceptions.DisambiguationError:
                vk.messages.send(
                    chat_id = event.chat_id,
                    message = 'Сам понял, че сказал ? Холера... Давай нормальный вопрос !!!',
                    random_id = 0
                )
            except wikipedia.exceptions.PageError:
                vk.messages.send(
                    chat_id = event.chat_id,
                    message = 'Сам понял, че сказал ? Холера... Давай нормальный вопрос !!!',
                    random_id = 0
                )


if __name__ == '__main__':
    # linking to vk
    vk_session = vk_api.VkApi(token = token)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    main()

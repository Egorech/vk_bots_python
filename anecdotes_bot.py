# import all the libraries for the vk_api
import vk_api
from vk_api.longpoll import VkLongPoll , VkEventType
from vk_api.keyboard import VkKeyboard , VkKeyboardColor

# libraries to select anecdotes and output a random
from anecdotes import anekdot_stirletz , anekdot_sport , anekdot_student
from random import randint

# libraries with vk token and vk group_id
import  _token

# necessary global variables for the chatbot
group_id = _token.group_id
token = _token.token

def main():
    """
    parsing the data was done in parser_anecdotes.py,
    but the anecdotes themselves were written into another file for speed, the file is called anecdotes.py
    """

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.text == 'Анекдот про Штирлица':
            vk.messages.send(
                user_id = event.user_id ,
                message = anekdot_stirletz[randint(1 , len(anekdot_stirletz) - 1)]
                , random_id = 0
                , keyboard = keyboard.get_keyboard()
            )
        elif event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.text == 'Анекдот про спорт':
            vk.messages.send(
                user_id = event.user_id ,
                message = anekdot_sport[randint(1 , len(anekdot_sport) - 1)]
                , random_id = 0
                , keyboard = keyboard.get_keyboard()
            )
        elif event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.text == 'Анекдот про студентов':
            vk.messages.send(
                user_id = event.user_id ,
                message = anekdot_student[randint(1 , len(anekdot_student) - 1)]
                , random_id = 0
                , keyboard = keyboard.get_keyboard()
            )
        elif event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            vk.messages.send(
                user_id = event.user_id ,
                message = "Такого варианта нет, холера..."
                , random_id = 0
                , keyboard = keyboard.get_keyboard()
            )


if __name__ == '__main__':

    # keyboard for the anecdote bot
    keyboard = VkKeyboard(one_time = False)
    keyboard.add_button('Анекдот про Штирлица' , color = VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Анекдот про спорт' , color = VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Анекдот про студентов' , color = VkKeyboardColor.PRIMARY)

    # linking to vk
    vk_session = vk_api.VkApi(token = token)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    main()

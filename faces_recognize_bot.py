# parsing libraries
import requests
from bs4 import BeautifulSoup

# import all the libraries for the vk_api
import vk_api
from vk_api.longpoll import VkLongPoll , VkEventType

import cv2

import  _token

# necessary global variables for the chatbot
group_id = _token.group_id
token = _token.token


def send_photo( photo1 ):
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
    function that repeats the message
    """

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            msg = vk.messages.getById(message_ids = event.message_id)

            url = msg['items'][0]['attachments'][0]['photo']['sizes'][-1]['url']

            r = requests.get(url , stream = True)

            with open('images/1.jpg' , 'bw') as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
            img = cv2.imread('images/1.jpg')

            dimensions = img.shape
            print(dimensions[:2])

            # обученная нейронная сеть, взятая с opencv, которая обучена распознавать лица
            faces = cv2.CascadeClassifier('front_face.xml')

            # координаты всех найденных объектов
            results = faces.detectMultiScale(img , scaleFactor = 2 ,
                                             minNeighbors = 1)

            # выделяем лица красной рамкой
            for (x , y , w , h) in results:
                cv2.rectangle(img , (x , y) , (x + w , y + h) , (0 , 0 , 255) ,
                              thickness = 2)

            # выводим фото на экран
            cv2.imwrite("images/1.jpg" , img)

            send_photo('images/1.jpg')
            vk.messages.send(
                chat_id = event.chat_id ,
                random_id = 0 ,
                attachment = attachment
            )

if __name__ == '__main__':

    # linking to vk
    vk_session = vk_api.VkApi(token = token)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    main()



# import all the libraries for the vk_api
import keras.models
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

# libraries with vk token and vk group_id
import _token

# necessary global variables for the chatbot
group_id = _token.group_id
token = _token.token

# parsing libraries
import requests
from bs4 import BeautifulSoup

# Avoiding downloading additional software represented by CUDO
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# photo size for the best grid performance
SIZE = 224

# all neural network libraries
import numpy as np
from keras.utils import load_img, img_to_array
import tensorflow_datasets as tfds
import tensorflow as tf


def resize_image(img):
    """
    function to change the training sample to a resolution of 224 by 224
    (at these values this neural network shows the best accuracy), and
    the color gradations were normalized by dividing by 255 so that
    the neural network sees colors from 0 to 1 inclusive
    """

    img = tf.cast(img, tf.float32)
    img = tf.image.resize(img, (SIZE, SIZE))
    img = img / 255.0
    return img


def ai_work():
    """
    function for work with photo
    """

    img = load_img('images/cat_dog_photo.png')
    img_array = img_to_array(img)
    img_resized = resize_image(img_array)
    img_expended = np.expand_dims(img_resized, axis = 0)
    prediction = model_loaded.predict(img_expended)[0][0]
    pred_label = 'Котик' if prediction < 0.5 else 'Собакен'
    return pred_label


def main():
    """
    cat/dog classification bot
    """

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                # search url at vk
                msg = vk.messages.getById(message_ids = event.message_id)
                url = msg['items'][0]['attachments'][0]['photo']['sizes'][-1]['url']

                # write the photo using the url to the images folder, name it cat_dog_photo.png
                r = requests.get(url, stream = True)
                with open('images/cat_dog_photo.png', 'bw') as f:
                    for chunk in r.iter_content(8192):
                        f.write(chunk)

                vk.messages.send(
                    chat_id = event.chat_id,
                    message = ai_work()
                    , random_id = 0
                )

            except IndexError:
                vk.messages.send(
                    chat_id = event.chat_id,
                    message = 'Бот предназначен для классификации кошек/собак.'
                    , random_id = 0
                )


if __name__ == '__main__':
    # linking to vk
    vk_session = vk_api.VkApi(token = token)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    # convolutional neural network for classifying cats/dogs, to speed up the work, the model is already trained,
    # you can find the implementation itself in the file neural_network.py
    model_loaded = keras.models.load_model('model_load')

    main()

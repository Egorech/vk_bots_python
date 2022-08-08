# import all the libraries for the vk_api
import vk_api
from vk_api.longpoll import VkLongPoll , VkEventType

# libraries with vk token and vk group_id
import  _token

# necessary global variables for the chatbot
group_id = _token.group_id
token = _token.token


import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from keras.utils import load_img, img_to_array
from keras.layers import Dense, GlobalAveragePooling2D, Dropout



train, _ = tfds.load('cats_vs_dogs', split=['train[:100%]'], with_info=True, as_supervised=True)


SIZE = 224

def resize_image(img, label):
  img = tf.cast(img, tf.float32)
  img = tf.image.resize(img, (SIZE, SIZE))
  img = img / 255.0
  return img, label


train_resized = train[0].map(resize_image)
train_batches = train_resized.shuffle(1000).batch(16)


base_layers = tf.keras.applications.MobileNetV2(input_shape=(SIZE, SIZE, 3), include_top=False)
base_layers.trainable = False


model = tf.keras.Sequential([
                             base_layers,
                             GlobalAveragePooling2D(),
                             Dropout(0.2),
                             Dense(1)
])
model.compile(optimizer='adam', loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), metrics=['accuracy'])


model.fit(train_batches, epochs=1)

img = load_img('images/img_2.png')
img_array = img_to_array(img)
img_resized, _ = resize_image(img_array, _)
img_expended = np.expand_dims(img_resized, axis=0)
prediction = model.predict(img_expended)[0][0]
pred_label = 'КОТ' if prediction < 0.5 else 'СОБАКА'
print(pred_label)
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

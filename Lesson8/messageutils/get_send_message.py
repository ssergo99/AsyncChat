import json
import time
import sys
import os

sys.path.append(os.path.join(os.getcwd(), '..'))
from deco_func import log


# @log
def get_msg(client):
    encoded_response = client.recv(1024)
    return encoded_response


# @log
def send_msg(new_socket, message_to_send):
    json_message = json.dumps(message_to_send)
    enc_message_to_send = json_message.encode('utf-8')
    new_socket.send(enc_message_to_send)


# @log
def msg_mkr(user_name='Anonymous', type_of_msg='presence'):
    if type_of_msg == 'chat_msg':
        msg_to_send = input('Введите сообщение: ')
        trg_user = input('Укажите получателя сообщения:   ')
        session_dict_msg = {
            'action': 'message',
            'time': time.time(),
            'author': user_name,
            'target_user': trg_user,
            'post_text': msg_to_send
        }
        return session_dict_msg
    else:
        prsnce_msg = {
            'action': 'presence',
            'time': time.time(),
            'user': user_name,
        }
        return prsnce_msg

import json
import sys
import os

sys.path.append(os.path.join(os.getcwd(), '..'))
from deco_func import log


@log
def check_msg(message):
    if isinstance(message, bytes):
        dec_message = message.decode('utf-8')
        load_message = json.loads(dec_message)
        if isinstance(load_message, dict):
            return load_message
        raise ValueError
    raise ValueError


@log
def check_client_message(message):
    if 'action' in message and message['action'] == 'presence' and 'time' in message \
            and 'user' in message:
        return {'response': 200}
    elif 'action' in message and message['action'] == 'message' and \
            'time' in message and 'author' in message and 'post_text' in message:
        return message
    return {
        'response': 400,
        'error': 'Bad Request'
    }


@log
def serv_response_check(message):
    if 'response' in message:
        if message['response'] == 200:
            return 'Success'
        return f'400, error: {message["error"]}'
    raise ValueError

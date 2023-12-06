import json


def check_msg(client):
    encoded_response = client.recv(1024)
    if isinstance(encoded_response, bytes):
        dec_message = encoded_response.decode('utf-8')
        load_message = json.loads(dec_message)
        if isinstance(load_message, dict):
            return load_message
        raise ValueError
    raise ValueError


def check_client_message(message):
    if 'action' in message and message['action'] == 'presence' and 'time' in message \
            and 'user' in message:
        return {'response': 200}
    elif 'action' in message and message['action'] == 'message' \
            and 'post_text' in message:
        return {'response': 200}
    return {
        'response': 400,
        'error': 'Bad Request'
    }


def serv_response_check(enc_resp):
    if isinstance(enc_resp, bytes):
        dec_resp = enc_resp.decode('utf-8')
        load_resp = json.loads(dec_resp)
        if 'response' in load_resp:
            if load_resp['response'] == 200:
                return 'Success'
            elif load_resp['response'] == 'Такой пользователь уже в чате':
                return 'Такой пользователь уже в чате'
            return f'Ответ сервера: {load_resp["error"]}'
    # raise ValueError

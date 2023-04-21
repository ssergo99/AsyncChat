"""

Клиентская часть программы:
установка соединений, проверка присутствия,
получение сообщений от сервера, проверка и отправка сообщений

 """

import sys
from time import time
from socket import *
from messageutils.check_message import serv_response_check, check_msg
from messageutils.get_send_message import get_msg, send_msg, msg_mkr
import logging
from random import randrange
import log.client_log_config
from deco_func import log

# Создаем объект-логгер:
logger_cl_obj = logging.getLogger('app.clientside')


# @log
def create_prs(user_name='Anonymous', user_status='Ready for talk'):
    logger_cl_obj.info('Создаем пресенс-соединение')
    session_dict = {
        'action': 'presence',
        'time': time(),
        'user': {
            'account_name': user_name,
            'status': user_status,
        }
    }
    return session_dict


def ans_from_users(message):
    if 'action' in message and message['action'] == 'message' and \
            'author' in message and 'post_text' in message:
        logger_cl_obj.info(f'Cообщение {message["post_text"]} от автора {message["author"]}')
        print(f'{message["author"]}: {message["post_text"]}')


# @log
def start_proc():
    try:
        logger_cl_obj.info('Старт проверки аргументов с адресом и портом')
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        type_of_cl = sys.argv[3]
        if type_of_cl == 'snd':
            m = randrange(65000)
            username = 'User' + str(m)
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except ValueError:
        logger_cl_obj.critical('Неверный номер порта')
        sys.exit(1)
    except IndexError:
        server_address = '127.0.0.1'
        server_port = 7777
        type_of_cl = 'snd'
        logger_cl_obj.info('Установлен адрес и порт по умолчанию: 127.0.0.1: 7777, '
                           'режим работы - отправка сообщений')
    try:
        to_serv_sock = socket(AF_INET, SOCK_STREAM)
        to_serv_sock.connect((server_address, server_port))
        logger_cl_obj.info(f'Установлено соединение по адресу: {server_address}:{server_port}')


    except ConnectionRefusedError:
        logger_cl_obj.critical('Сервер недоступен')
        sys.exit(1)
    else:
        while True:
            if type_of_cl == 'snd':
                try:
                    msg_of_auth = msg_mkr(username)
                    send_msg(to_serv_sock, msg_of_auth)
                    data = to_serv_sock.recv(1024).decode('utf-8')
                    logger_cl_obj.error(f'Ответ сервера {data}.')
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    logger_cl_obj.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)
            if type_of_cl == 'rcv':
                try:
                    ans_from_users(check_msg(get_msg(to_serv_sock)))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    logger_cl_obj.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    start_proc()

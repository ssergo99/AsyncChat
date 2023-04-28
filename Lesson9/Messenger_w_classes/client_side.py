"""

Клиентская часть программы:
установка соединений, проверка присутствия,
получение сообщений от сервера, проверка и отправка сообщений

 """

import sys
from threading import Thread
from time import sleep, time
from socket import *
from messageutils.check_message import serv_response_check, check_msg
from messageutils.get_send_message import get_msg, send_msg
import logging
import log.client_log_config
from deco_func import LogClass

# Создаем объект-логгер:
logger_cl_obj = logging.getLogger('app.clientside')


class MessageClass:
    def __init__(self, user_name):
        self.user_name = user_name
        self.type_of_msg = ''
        self.action = ''
        self.time = time()
        self.msg_dict = dict()

    def msg_maker(self, type_of_msg):
        self.type_of_msg = type_of_msg
        self.time = time()
        if self.type_of_msg == 'chat_msg':
            self.action = 'message'
            msg_to_send = input('Введите сообщение в чат: ')
            session_dict_msg = {
                'action': self.action,
                'time': self.time,
                'author': self.user_name,
                'post_text': msg_to_send
            }
            self.msg_dict = session_dict_msg
        else:
            self.action = 'presence'
            prsnce_msg = {
                'action': self.action,
                'time': self.time,
                'user': self.user_name,
            }
            self.msg_dict = prsnce_msg
        return self.msg_dict


class ChatThread(Thread):
    def __init__(self, func, sock, name=None):
        super().__init__()
        self.daemon = True
        self.func_targ = func
        self.socket = sock
        self.username = name

    def run(self):
        if not self.username:
            self.func_targ(self.socket)
        else:
            self.func_targ(self.socket, self.username)


@LogClass()
def parsing_cl_arguments():
    logger_cl_obj.info('Старт проверки аргументов с адресом и портом')
    server_address = '127.0.0.1'
    server_port = 7777
    cl_type = 'rcv'
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        cl_type = sys.argv[3]
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except ValueError:
        logger_cl_obj.critical('Неверный номер порта')
        sys.exit(1)
    except IndexError:
        logger_cl_obj.info('Установлен адрес и порт по умолчанию: 127.0.0.1: 7777, '
                           'тип клиента - читающий чат ')
    return server_address, server_port, cl_type


@LogClass()
def ans_from_users(message):
    if 'action' in message and message['action'] == 'message' and \
            'author' in message and 'post_text' in message:
        logger_cl_obj.info(f'Cообщение {message["post_text"]} от автора {message["author"]}')
        print(f'Сообщение из чата: {message["author"]} >>> {message["post_text"]}')


@LogClass()
def rcv_messages_from_chat(from_chat_sock):
    while True:
        try:
            ans_from_users(check_msg(from_chat_sock))
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
            sys.exit(1)


@LogClass()
def send_messages_to_chat(to_chat_sock, username):
    while True:
        try:
            msg_to_chat1 = MessageClass(username)
            msg_of_auth = msg_to_chat1.msg_maker('chat_msg')
            send_msg(to_chat_sock, msg_of_auth)
            sleep(2.5)
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
            sys.exit(1)


@LogClass()
def start_proc():
    server_address, server_port, type_of_cl = parsing_cl_arguments()
    username = input('Введите свое имя для чата:    ')
    prs_msg_of_user = MessageClass(username)
    try:
        print(f'Получены аргументы: {server_address}:{server_port}')
        to_serv_sock = socket(AF_INET, SOCK_STREAM)
        print(f'Создан сокет: {to_serv_sock}')
        to_serv_sock.connect((server_address, server_port))
        print(f'Установлено соединение по адресу: {server_address}:{server_port}')
        logger_cl_obj.info(f'Установлено соединение по адресу: {server_address}:{server_port}')
        send_msg(to_serv_sock, prs_msg_of_user.msg_maker('presence'))
        data = serv_response_check(get_msg(to_serv_sock))
        logger_cl_obj.debug(f'Ответ сервера {data}.')

    except ConnectionRefusedError:
        logger_cl_obj.critical('Сервер недоступен')
        sys.exit(1)
    else:
        if type_of_cl == 'rcv':
            thr_msg_receiver = ChatThread(rcv_messages_from_chat, to_serv_sock)
            thr_msg_receiver.start()
            while True:
                sleep(1)
                if thr_msg_receiver.is_alive():
                    continue
                break
        else:

            thr_msg_sender = ChatThread(send_messages_to_chat, to_serv_sock, username)
            thr_msg_sender.start()
            while True:
                sleep(1)
                if thr_msg_sender.is_alive():
                    continue
                break


if __name__ == '__main__':
    start_proc()

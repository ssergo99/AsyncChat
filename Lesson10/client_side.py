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
from clmeta import ClientVerifier

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


class Client(Thread, metaclass=ClientVerifier):
    def __init__(self, func=None, sock=None, name=None):
        super().__init__()
        self.daemon = True
        self.func_targ = func
        self.socket = sock
        self.username = name
        self.type_cl = ''
        self.srv_add = ''
        self.serv_port = int

    def run(self):
        if self.type_cl == 'rcv':
            self.func_targ(self.socket)
        else:
            self.func_targ(self.socket, self.username)

    def start_proc(self):
        prs_msg_of_user = MessageClass(self.username)
        send_msg(self.socket, prs_msg_of_user.msg_maker('presence'))
        data = serv_response_check(get_msg(self.socket))
        logger_cl_obj.debug(f'Ответ сервера {data}.')
        if self.type_cl == 'rcv':
            self.func_targ = rcv_messages_from_chat
            self.run()
            while True:
                sleep(1)
                if self.is_alive():
                    continue
                break
        else:
            self.func_targ = send_messages_to_chat
            self.run()
            while True:
                sleep(1)
                if self.is_alive():
                    continue
                break


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


def start_socket(server_address, server_port):
    try:
        print(f'Получены аргументы: {server_address}:{server_port}')
        new_socket = socket(AF_INET, SOCK_STREAM)
        print(f'Создан сокет: {socket}')
        new_socket.connect((server_address, server_port))
        print(f'Установлено соединение по адресу: {server_address}:{server_port}')
        logger_cl_obj.info(f'Установлено соединение по адресу: {server_address}:{server_port}')
    except ConnectionRefusedError:
        logger_cl_obj.critical('Сервер недоступен')
        sys.exit(1)
    return new_socket


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
def main_start():
    server_address, server_port, type_of_cl = parsing_cl_arguments()
    username = input('Введите свое имя для чата:    ')
    client1 = Client(func=None, sock=None, name=username)
    client1.srv_add = server_address
    client1.serv_port = server_port
    client1.type_cl = type_of_cl
    client1.socket = start_socket(client1.srv_add, client1.serv_port)
    client1.start_proc()


if __name__ == '__main__':
    main_start()

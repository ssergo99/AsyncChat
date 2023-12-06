"""

Клиентская часть программы:
установка соединений, проверка присутствия,
получение сообщений от сервера, проверка и отправка сообщений

 """
import hashlib
import os
import sys
from threading import Thread
from time import sleep, time
from socket import *

from cl_chat_ui import InputUserName, ClientMainWindow
from messageutils.check_message import serv_response_check, check_msg
from messageutils.get_send_message import get_msg, send_msg
import logging
import log.client_log_config
from deco_func import LogClass
from clmeta import ClientVerifier
from cl_db import ClStorage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QObject
from Cryptodome.PublicKey import RSA

# Создаем объект-логгер:
logger_cl_obj = logging.getLogger('app.clientside')

USER_INTER_VAR = """
Для выбора действия введите одно из следующих значений: 
Написать соощение - send
Создать контакт - create
Удалить контакт - delete
Получить список своих контактов - contact
Получить список своих логинов - logins
Получить список активных пользователей  - active
Выйти из чата - exit
"""


class MessageClass:
    def __init__(self, user_name):
        self.user_name = user_name
        self.cont_name = ''
        self.type_of_msg = ''
        self.action = ''
        self.time = time()
        self.msg_to_send = ''
        self.msg_dict = dict()
        self.to_users_index = False
        self.logout_index = False

    def msg_maker(self, type_of_msg, passw=None, keys=None):
        self.type_of_msg = type_of_msg
        self.time = time()
        if self.type_of_msg == 'chat_msg':
            self.action = 'message'
            print(f'------------Чат пользователя {self.user_name}---------------')
            user_choice = input(USER_INTER_VAR)
            if user_choice == 'contact':
                session_dict_msg = {
                    'action': self.action,
                    'time': self.time,
                    'author': self.user_name,
                    'send_to': self.cont_name,
                    'to_users': self.to_users_index,
                    'post_text': '@contact@',
                    'logout': self.logout_index
                }
                self.msg_dict = session_dict_msg
            elif user_choice == 'logins':
                session_dict_msg = {
                    'action': self.action,
                    'time': self.time,
                    'author': self.user_name,
                    'send_to': self.cont_name,
                    'to_users': self.to_users_index,
                    'post_text': '@logins@',
                    'logout': self.logout_index
                }
                self.msg_dict = session_dict_msg
            elif user_choice == 'active':
                session_dict_msg = {
                    'action': self.action,
                    'time': self.time,
                    'author': self.user_name,
                    'send_to': self.cont_name,
                    'to_users': self.to_users_index,
                    'post_text': '@active@',
                    'logout': self.logout_index
                }
                self.msg_dict = session_dict_msg
            elif user_choice == 'create':
                self.cont_name = input('Какого пользователя добавить в контакты?: ')
                session_dict_msg = {
                    'action': self.action,
                    'time': self.time,
                    'author': self.user_name,
                    'send_to': self.cont_name,
                    'to_users': self.to_users_index,
                    'post_text': '@create@',
                    'logout': self.logout_index
                }
                self.msg_dict = session_dict_msg
            elif user_choice == 'delete':
                self.cont_name = input('Какого пользователя удалить из контактов?: ')
                session_dict_msg = {
                    'action': self.action,
                    'time': self.time,
                    'author': self.user_name,
                    'send_to': self.cont_name,
                    'to_users': self.to_users_index,
                    'post_text': '@delete@',
                    'logout': self.logout_index
                }
                self.msg_dict = session_dict_msg
            elif user_choice == 'exit':
                self.logout_index = True
                session_dict_msg = {
                    'action': self.action,
                    'time': self.time,
                    'author': self.user_name,
                    'send_to': self.cont_name,
                    'to_users': self.to_users_index,
                    'post_text': '@exit@',
                    'logout': self.logout_index
                }
                self.msg_dict = session_dict_msg
            elif user_choice == 'send':
                self.cont_name = input('Какому пользователю отправить сообщение?: ')
                self.msg_to_send = input('Введите сообщение в чат (для выхода из чата напишите ВЫХОД): ')
                if self.msg_to_send == 'ВЫХОД':
                    self.logout_index = True
                else:
                    self.to_users_index = True
                session_dict_msg = {
                    'action': self.action,
                    'time': self.time,
                    'author': self.user_name,
                    'send_to': self.cont_name,
                    'to_users': self.to_users_index,
                    'post_text': self.msg_to_send,
                    'logout': self.logout_index
                }
                self.msg_dict = session_dict_msg
            else:
                print('Некорректный параметр. Вы отключены от чата')
                self.logout_index = True
                session_dict_msg = {
                    'action': self.action,
                    'time': self.time,
                    'author': self.user_name,
                    'send_to': self.cont_name,
                    'to_users': self.to_users_index,
                    'post_text': self.msg_to_send,
                    'logout': self.logout_index
                }
                self.msg_dict = session_dict_msg
        else:
            self.action = 'presence'
            prsnce_msg = {
                'action': self.action,
                'time': self.time,
                'user': self.user_name,
                'pass': passw,
                'keys': keys
            }
            self.msg_dict = prsnce_msg
        return self.msg_dict


class Client(Thread, QObject):
    new_message = pyqtSignal(dict)
    connection_lost = pyqtSignal()

    def __init__(self, cl_db, passwd, keys, rcv_func=None, snd_func=None, sock=None, name=None):
        Thread.__init__(self)
        QObject.__init__(self)
        self.daemon = True
        self.rcv_func_targ = rcv_func
        self.snd_func_targ = snd_func
        self.socket = sock
        self.username = name
        self.srv_add = ''
        self.serv_port = int
        self.cl_db = cl_db
        self.passwd = passwd
        self.keys = keys

    def run(self):
        self.rcv_func_targ(self.socket, self.cl_db, self)
        self.snd_func_targ(self.socket, self.username, self.cl_db)

    def start_proc(self):
        prs_msg_of_user = MessageClass(self.username)
        m = prs_msg_of_user.msg_maker('presence', passw= self.passwd, keys=self.keys)
        send_msg(self.socket, m)
        data = serv_response_check(get_msg(self.socket))
        if data == 'Такой пользователь уже в чате':
            print(data)
            sys.exit(1)
        else:
            logger_cl_obj.debug(f'Ответ сервера {data}.')
            self.rcv_func_targ = rcv_messages_from_chat
        self.snd_func_targ = send_messages_to_chat

    def add_contact(self, cont):
        session_dict_msg2 = {
            'action': 'message',
            'time': time(),
            'author': self.username,
            'send_to': cont,
            'to_users': False,
            'post_text': '@create@',
            'logout': False
        }
        send_msg(self.socket, session_dict_msg2)

    def get_p_key(self, cont2):
        session_dict_msg2 = {
            'action': 'message',
            'time': time(),
            'author': self.username,
            'send_to': cont2,
            'to_users': False,
            'post_text': '@pub_key@',
            'logout': False
        }
        send_msg(self.socket, session_dict_msg2)
        serv_answer6 = check_msg(self.socket)
        return serv_answer6['pub_key']

    def delete_contact(self, cont2):
        session_dict_msg2 = {
            'action': 'message',
            'time': time(),
            'author': self.username,
            'send_to': cont2,
            'to_users': False,
            'post_text': '@delete@',
            'logout': False
        }
        send_msg(self.socket, session_dict_msg2)

    def send_message(self, receiver, mess):
        session_dict_msg3 = {
            'action': 'message',
            'time': time(),
            'author': self.username,
            'send_to': receiver,
            'to_users': True,
            'post_text': mess,
            'logout': False
        }
        send_msg(self.socket, session_dict_msg3)

    def get_users_from_server(self, username):
        request22 = {
            'action': 'message',
            'time': time(),
            'author': username,
            'post_text': '@list_of_users@',
            'logout': False
        }
        send_msg(self.socket, request22)
        serv_answer3 = check_msg(self.socket)
        return serv_answer3['users_list']

    def check_users_in_chat(self, user_to_check):
        session_dict_msg4 = {
            'action': 'message',
            'time': time(),
            'author': self.username,
            'send_to': 'server',
            'to_users': False,
            'post_text': '@active@',
            'logout': False
        }
        send_msg(self.socket, session_dict_msg4)
        serv_answer3 = check_msg(self.socket)
        try:
            if serv_answer3['usrs_in_chat'].count(user_to_check) > 0:
                return True
            else:
                return False
        except KeyError:
            return False




@LogClass()
def parsing_cl_arguments():
    logger_cl_obj.info('Старт проверки аргументов с адресом и портом')
    server_address = '127.0.0.1'
    server_port = 7777
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except ValueError:
        logger_cl_obj.critical('Неверный номер порта')
        sys.exit(1)
    except IndexError:
        logger_cl_obj.info('Установлен адрес и порт по умолчанию: 127.0.0.1: 7777, '
                           'тип клиента - читающий чат ')
    return server_address, server_port


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
            'author' in message and message['author'] != 'server' and 'post_text' in message:
        logger_cl_obj.info(f'Cообщение {message["post_text"]} от автора {message["author"]}')
        print(f'Сообщение из чата: {message["author"]} >>> {message["post_text"]}')
    elif 'action' in message and message['action'] == 'message' and \
            message['author'] == 'server' and 'post_text' in message:
        logger_cl_obj.info(f'Cообщение {message["post_text"]} от сервера')
        print(f'Ответ сервера: {message["post_text"]}')
    elif 'action' in message and message['action'] == 'active' and \
            'author' in message and 'post_text' in message:
        print(f'Сейчас в чате следующие пользователи: >>> {message["post_text"]}')
    elif 'action' in message and message['action'] == 'contact' and \
            'author' in message and 'post_text' in message:
        print(f'В вашем контактном листе следующие пользователи: >>> {message["post_text"]}')
    elif 'action' in message and message['action'] == 'logins' and \
            'author' in message and 'post_text' in message:
        print(f'Список ваших логинов: >>> {message["post_text"]}')
    elif 'response' in message:
        print(f'Код от сервера: >>> {message["response"]}')


@LogClass()
def rcv_messages_from_chat(from_chat_sock, db_cl, cl):
    while True:
        try:
            msg = check_msg(from_chat_sock)
            # ans_from_users(msg)
            if 'action' in msg and msg['action'] == 'message' and \
                    'author' in msg and msg['author'] != 'server' and 'post_text' in msg:
                cl.new_message.emit(msg)
            if 'disconnect' in msg:
                sys.exit(1)
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
            sys.exit(1)


@LogClass()
def send_messages_to_chat(to_chat_sock, username, cl_db_1):
    while True:
        try:
            msg_to_chat1 = MessageClass(username)
            msg_of_auth = msg_to_chat1.msg_maker('chat_msg')
            if msg_of_auth['to_users']:
                cl_db_1.store_message_in_db(msg_of_auth['send_to'],
                                            False,
                                            msg_of_auth['post_text'])
                send_msg(to_chat_sock, msg_of_auth)
            elif msg_of_auth['post_text'] == '@create@':
                if not cl_db_1.check_contact(msg_of_auth['send_to']):
                    cl_db_1.add_contact(msg_of_auth['send_to'])
                    send_msg(to_chat_sock, msg_of_auth)

            elif msg_of_auth['post_text'] == '@delete@':
                if cl_db_1.check_contact(msg_of_auth['send_to']):
                    cl_db_1.del_contact(msg_of_auth['send_to'])
                    send_msg(to_chat_sock, msg_of_auth)
            else:
                send_msg(to_chat_sock, msg_of_auth)
            if msg_of_auth['logout']:
                break
            sleep(2.5)
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
            sys.exit(1)


def generate_hash2(pass_to_hash):
    passwd_bt = pass_to_hash.encode('utf-8')
    to_salt = 'simple_salt'
    salt = to_salt.encode('utf-8')
    passwd_hash = hashlib.pbkdf2_hmac('sha512', passwd_bt, salt, 1000)
    passwd_hash_str = passwd_hash.hex()
    return passwd_hash_str


# def get_contacts_from_server(socket1, username):
#     request = {
#         'action': 'message',
#         'time': time(),
#         'author': username,
#         'post_text': '@list_of_cont@',
#         'logout': False
#     }
#     send_msg(socket1, request)
#     serv_answer = check_msg(socket1)
#     return serv_answer['contact_list']


# def get_users_from_server(socket2, username):
#     request2 = {
#         'action': 'message',
#         'time': time(),
#         'author': username,
#         'post_text': '@list_of_users@',
#         'logout': False
#     }
#     send_msg(socket2, request2)
#     serv_answer2 = check_msg(socket2)
#     return serv_answer2['users_list']


@LogClass()
def main_start():
    server_address, server_port = parsing_cl_arguments()
    cl_app = QApplication(sys.argv)
    usr_name_inp = InputUserName(server_address, server_port)
    cl_app.exec_()
    if usr_name_inp.approved:
        username = usr_name_inp.username.text()
        pass1 = generate_hash2(usr_name_inp.passwd.text())
        del usr_name_inp
        cl_app.quit()
    else:
        sys.exit(0)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    key_file = os.path.join(dir_path, f'{username}.key')
    if not os.path.exists(key_file):
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as key:
            key.write(keys.export_key())
    else:
        with open(key_file, 'rb') as key:
            keys = RSA.import_key(key.read())

    pubkey = keys.publickey().export_key().decode('ascii')
    cl_db1 = ClStorage(username)
    client1 = Client(cl_db1, pass1, pubkey, rcv_func=None, snd_func=None, sock=None, name=username)
    client1.srv_add = server_address
    client1.serv_port = server_port
    client1.socket = start_socket(client1.srv_add, client1.serv_port)
    # contact_list = get_contacts_from_server(client1.socket, username)
    # cl_db1.make_contact_from_serv(contact_list)
    client1.start_proc()
    client1.start()
    users_list = client1.get_users_from_server(username)
    cl_db1.fill_users_from_serv(users_list)
    main_window = ClientMainWindow(cl_db1, client1, username, keys)
    main_window.make_connection(client1)
    main_window.setWindowTitle(f'Чат пользователя {username}')
    cl_app.exec_()
    while True:
        sleep(1)
        if client1.is_alive():
            continue
        break


if __name__ == '__main__':
    main_start()

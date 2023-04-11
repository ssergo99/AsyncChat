"""

Клиентская часть программы:
установка соединений, проверка присутствия,
получение сообщений от сервера, проверка и отправка сообщений

 """

import sys
from time import time
from socket import *
from messageutils.check_message import serv_response_check, check_msg
from messageutils.get_send_message import get_msg, send_msg


def create_prs(user_name='Anonymous', user_status='Ready for talk'):
    session_dict = {
        'action': 'presence',
        'time': time(),
        'user': {
            'account_name': user_name,
            'status': user_status,
        }
    }
    return session_dict


def start_proc():
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except ValueError:
        print('Неверный номер порта')
        sys.exit(1)
    except IndexError:
        server_address = '127.0.0.1'
        server_port = 7777

    try:
        to_serv_sock = socket(AF_INET, SOCK_STREAM)
        to_serv_sock.connect((server_address, server_port))
        msg_to_server = create_prs()
        send_msg(to_serv_sock, msg_to_server)
        new_response = serv_response_check(check_msg(get_msg(to_serv_sock)))
        print(new_response)

        to_serv_sock1 = socket(AF_INET, SOCK_STREAM)
        to_serv_sock1.connect((server_address, server_port))
        msg_to_server1 = create_prs('User1', 'Do not disturb')
        send_msg(to_serv_sock1, msg_to_server1)
        new_response1 = serv_response_check(check_msg(get_msg(to_serv_sock1)))
        print(new_response1)
    except ConnectionRefusedError:
        print('Сервер недоступен')
        sys.exit(1)


if __name__ == '__main__':
    start_proc()

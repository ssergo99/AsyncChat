"""

Cерверная часть программы:
проверка аттрибутов, установка соединения,
получение сообщений, проверка и отправка сообщений клиенту

 """

import sys
from datetime import datetime
from socket import *
from messageutils.check_message import check_client_message, check_msg
from messageutils.get_send_message import get_msg, send_msg


def start_proc():
    try:
        if '-a' in sys.argv:
            srv_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            print('Установлен адрес по умолчанию - 127.0.0.1')
            srv_address = '127.0.0.1'
        if '-p' in sys.argv:
            serv_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            print('Установлен номер порта по умолчанию - 7777')
            serv_port = 7777
        if serv_port < 1024 or serv_port > 65535:
            raise ValueError
    except ValueError:
        print(
            'Неверный номер порта')
        sys.exit(1)
    except IndexError:
        print('Укажите номер порта/адреса после параметра.')
        sys.exit(1)

    serv_sock = socket(AF_INET, SOCK_STREAM)
    serv_sock.bind((srv_address, serv_port))
    serv_sock.listen(1024)
    print('Сервер запущен и ожидает входящих запросов.')

    while True:
        client, client_address = serv_sock.accept()
        message_from_client = check_msg(get_msg(client))
        utc_time = datetime.utcfromtimestamp(message_from_client['time'])
        print(f'=============================================================\n'
              f'Тип запроса: {message_from_client["action"]}\n'
              f'Время запроса: {utc_time.strftime("%d-%m-%Y %H:%M:%S")}\n'
              f'Пользователь: {message_from_client["user"]["account_name"]}\n'
              f'Статус пользователя: {message_from_client["user"]["status"]}\n')
        resp_to_client = check_client_message(message_from_client)
        send_msg(client, resp_to_client)
        client.close()


if __name__ == '__main__':
    start_proc()

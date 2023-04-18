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
import logging
import log.server_log_config
from deco_func import log

# Создаем объект-логгер:
logger_srv_obj = logging.getLogger('app.serverside')


@log
def start_proc_srv():
    logger_srv_obj.info('Считываем параметры адреса и порта, иначе - устанавливаем по умолчанию')
    try:
        if '-a' in sys.argv:
            srv_address = sys.argv[sys.argv.index('-a') + 1]
            logger_srv_obj.debug(f'Установлен адрес: {srv_address}')
        else:
            srv_address = '127.0.0.1'
            logger_srv_obj.info('Установлен адрес по умолчанию: 127.0.0.1')
        if '-p' in sys.argv:
            serv_port = int(sys.argv[sys.argv.index('-p') + 1])
            logger_srv_obj.debug(f'Установлен порт: {serv_port}')
        else:
            serv_port = 7777
            logger_srv_obj.info('Установлен порт по умолчанию: 7777')
        if serv_port < 1024 or serv_port > 65535:
            raise ValueError
    except ValueError:
        logger_srv_obj.critical('Неверный номер порта')
        sys.exit(1)
    except IndexError:
        logger_srv_obj.error('Укажите верный номер порта/адрес')
        sys.exit(1)

    serv_sock = socket(AF_INET, SOCK_STREAM)
    serv_sock.bind((srv_address, serv_port))
    serv_sock.listen(1024)
    logger_srv_obj.debug('Сервер запущен и ожидает входящих соединений')

    while True:
        client, client_address = serv_sock.accept()
        message_from_client = check_msg(get_msg(client))
        utc_time = datetime.utcfromtimestamp(message_from_client['time'])
        logger_srv_obj.info(f'Блок информации о запросе\n'
                            f'Тип запроса: {message_from_client["action"]}\n'
                            f'Время запроса: {utc_time.strftime("%d-%m-%Y %H:%M:%S")}\n'
                            f'Пользователь: {message_from_client["user"]["account_name"]}\n'
                            f'Статус пользователя: {message_from_client["user"]["status"]}\n')
        resp_to_client = check_client_message(message_from_client)
        send_msg(client, resp_to_client)
        client.close()


if __name__ == '__main__':
    start_proc_srv()

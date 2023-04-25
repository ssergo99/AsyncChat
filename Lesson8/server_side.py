"""

Cерверная часть программы:
проверка аттрибутов, установка соединения,
получение сообщений, проверка и отправка сообщений клиенту

 """
import select
import time
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


def parsing_arguments():
    logger_srv_obj.info('Считываем параметры адреса и порта, иначе - устанавливаем по умолчанию')
    try:
        srv_address = '127.0.0.1'
        serv_port = 7777
        if '-a' in sys.argv:
            srv_address = sys.argv[sys.argv.index('-a') + 1]
            logger_srv_obj.debug(f'Установлен адрес: {srv_address}')
        else:
            logger_srv_obj.info('Установлен адрес по умолчанию: 127.0.0.1')
        if '-p' in sys.argv:
            serv_port = int(sys.argv[sys.argv.index('-p') + 1])
            logger_srv_obj.debug(f'Установлен порт: {serv_port}')
            if serv_port < 1024 or serv_port > 65535:
                raise ValueError
        else:
            logger_srv_obj.info('Установлен порт по умолчанию: 7777')
    except ValueError:
        logger_srv_obj.critical('Неверный номер порта')
        sys.exit(1)
    except IndexError:
        logger_srv_obj.error('Укажите верный номер порта/адрес')
        sys.exit(1)
    return srv_address, serv_port


def start_proc_srv():
    srv_address, serv_port = parsing_arguments()
    serv_sock = socket(AF_INET, SOCK_STREAM)
    serv_sock.bind((srv_address, serv_port))
    serv_sock.settimeout(0.5)
    serv_sock.listen(1024)
    logger_srv_obj.debug('Сервер запущен и ожидает входящих соединений')

    cl_list = []
    msg_list = []
    users_in_chat = dict()

    while True:
        try:
            client, client_address = serv_sock.accept()
        except OSError as e:
            pass
        else:
            logger_srv_obj.info(f'Получен запрос на соединение с {client_address}')
            cl_list.append(client)
            logger_srv_obj.info(f'Лист клиентов {cl_list}')

        r = []
        w = []
        e = []

        try:
            if cl_list:
                r, w, e = select.select(cl_list, cl_list, [], 10)
                logger_srv_obj.info(f'Лист типов {r}, {w}, {e}')
        except:
            pass
        if r:
            for client_in_r in r:
                try:
                    new_msg = check_msg(client_in_r)
                    utc_time = datetime.utcfromtimestamp(new_msg['time'])
                    logger_srv_obj.info(f'action:{new_msg["action"]} time:{new_msg["time"]}')
                    if new_msg['action'] == 'presence':
                        users_in_chat[new_msg['user']] = client_in_r
                        logger_srv_obj.info(f'Пользователи в чате{users_in_chat}')
                        send_msg(client_in_r, check_client_message(new_msg))
                        logger_srv_obj.info(f'Блок информации о запросе\n'
                                            f'Тип запроса: {new_msg["action"]}\n'
                                            f'Время запроса: {utc_time.strftime("%d-%m-%Y %H:%M:%S")}\n'
                                            f'Пользователь: {new_msg["user"]}\n')
                    elif new_msg['action'] == 'message':
                        msg_from_cl = check_client_message(new_msg)
                        msg_list.append(msg_from_cl)
                        logger_srv_obj.info(f'Блок информации о запросе\n'
                                            f'Тип запроса: {msg_from_cl["action"]}\n'
                                            f'Время сообщения: {utc_time.strftime("%d-%m-%Y %H:%M:%S")}\n'
                                            f'Автор сообщения: {msg_from_cl["author"]}\n'
                                            f'Получатель сообщения: {msg_from_cl["target_user"]}\n'
                                            f'Текст сообщения: {msg_from_cl["post_text"]}\n')
                    else:
                        bad_response = {
                            'response': 400,
                            'error': 'Bad Request'
                        }
                        send_msg(client_in_r, bad_response)
                except:
                    pass
                    # logger_srv_obj.debug(f'Нет соединения с клиентом {client_in_r}')
                    # cl_list.remove(client_in_r)
        for msg_to_send in msg_list:
            try:
                if msg_to_send['target_user'] in users_in_chat:
                    # and users_in_chat[msg_to_send['target_user']] in w:\
                        send_msg(users_in_chat[msg_to_send['target_user']], msg_to_send)
            except:
                logger_srv_obj.debug(f'Нет соединения с клиентом {msg_to_send["target_user"]}')
                cl_list.remove(msg_to_send["target_user"])
        msg_list.clear()

if __name__ == '__main__':
    start_proc_srv()

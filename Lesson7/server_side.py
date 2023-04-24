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


def start_proc_srv():
    cl_list = []
    msg_list = []
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
    serv_sock.settimeout(0.5)
    logger_srv_obj.debug('Сервер запущен и ожидает входящих соединений')

    while True:
        try:
            client, client_address = serv_sock.accept()
        except OSError as e:
            pass
        else:
            logger_srv_obj.info(f'Получен запрос на соединение с {client_address}')
            cl_list.append(client)
            logger_srv_obj.info(f'Лист клиентов {cl_list}')

        finally:
            r = []
            w = []
            try:
                r, w, e = select.select(cl_list, cl_list, [], 10)
                logger_srv_obj.info(f'Лист типов {r}, {w}, {e}')
            except:
                pass
            if r:
                logger_srv_obj.info(f'{r}')
                for client_in_r in r:
                    try:
                        msg_from_cl = check_client_message(check_msg(get_msg(client_in_r)))
                        utc_time = datetime.utcfromtimestamp(msg_from_cl['time'])
                        if msg_from_cl['action'] == 'message':
                            msg_list.append(msg_from_cl)
                            logger_srv_obj.info(f'Блок информации о запросе\n'
                                                f'Тип запроса: {msg_from_cl["action"]}\n'
                                                f'Время сообщения: {utc_time.strftime("%d-%m-%Y %H:%M:%S")}\n'
                                                f'Автор сообщения: {msg_from_cl["author"]}\n'
                                                f'Текст сообщения: {msg_from_cl["post_text"]}\n')
                        else:
                            send_msg(client_in_r, msg_from_cl)
                            logger_srv_obj.info(f'Блок информации о запросе\n'
                                                f'Тип запроса: {msg_from_cl["action"]}\n'
                                                f'Время запроса: {utc_time.strftime("%d-%m-%Y %H:%M:%S")}\n'
                                                f'Пользователь: {msg_from_cl["user"]["account_name"]}\n'
                                                f'Статус пользователя: {msg_from_cl["user"]["status"]}\n')
                    except:
                        logger_srv_obj.debug(f'Нет соединения с клиентом {client_in_r}')
                        cl_list.remove(client_in_r)
            if msg_list and w:
                logger_srv_obj.info(f'{w} и {msg_list}')
                msg_to_send = {
                    'action': 'message',
                    'time': time.time(),
                    'author': msg_list[0]['author'],
                    'post_text': msg_list[0]['post_text']
                }
                del msg_list[0]
                for client_in_w in w:
                    try:
                        send_msg(client_in_w, msg_to_send)
                    except:
                        logger_srv_obj.debug(f'Нет соединения с клиентом {client_in_w}')
                        cl_list.remove(client_in_w)


if __name__ == '__main__':
    start_proc_srv()

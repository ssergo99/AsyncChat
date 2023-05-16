"""

Cерверная часть программы:
проверка аттрибутов, установка соединения,
получение сообщений, проверка и отправка сообщений клиенту

 """
import select
import sys
from datetime import datetime
from socket import *
from messageutils.check_message import check_client_message, check_msg
from messageutils.get_send_message import send_msg
import logging
import log.server_log_config
from deco_func import LogClass
from srvmeta import ServerVerifier
from descservsock import PortChecker

# Создаем объект-логгер:
logger_srv_obj = logging.getLogger('app.serverside')


@LogClass()
def parsing_arguments():
    logger_srv_obj.info('Считываем параметры адреса и порта, иначе - устанавливаем по умолчанию')
    try:
        s_address = '127.0.0.1'
        s_port = 7777
        if '-a' in sys.argv:
            s_address = sys.argv[sys.argv.index('-a') + 1]
            logger_srv_obj.debug(f'Установлен адрес: {s_address}')
        else:
            logger_srv_obj.info('Установлен адрес по умолчанию: 127.0.0.1')
        if '-p' in sys.argv:
            s_port = sys.argv[sys.argv.index('-p') + 1]
            logger_srv_obj.debug(f'Установлен порт: {s_port}')
        else:
            logger_srv_obj.info('Установлен порт по умолчанию: 7777')
    except ValueError:
        logger_srv_obj.critical('Неверный номер порта')
        sys.exit(1)
    except IndexError:
        logger_srv_obj.error('Укажите верный номер порта/адрес')
        sys.exit(1)
    return s_address, s_port


class Server(metaclass=ServerVerifier):
    serv_port = PortChecker()

    def __init__(self, sr_address, sr_port):
        self.srv_address = sr_address
        self.serv_port = sr_port
        self.cl_list = []
        self.msg_list = []
        self.users_in_chat = []
        self.sock = None

    def start_socket(self):
        logger_srv_obj.debug('Сервер запущен и ожидает входящих соединений')
        print('Сервер запущен и ожидает входящих соединений')
        serv_sock = socket(AF_INET, SOCK_STREAM)
        serv_sock.bind((self.srv_address, self.serv_port))
        serv_sock.settimeout(0.5)
        self.sock = serv_sock
        self.sock.listen()

    def start_proc_srv(self):
        self.start_socket()

        while True:
            try:
                client, client_address = self.sock.accept()
            except OSError as e:
                pass
            else:
                logger_srv_obj.info(f'Получен запрос на соединение с {client_address}')
                print(f'Получен запрос на соединение с {client_address}')
                self.cl_list.append(client)
                logger_srv_obj.info(f'Лист клиентов {self.cl_list}')

            r = []
            w = []
            e = []

            try:
                if self.cl_list:
                    r, w, e = select.select(self.cl_list, self.cl_list, [], 10)
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
                            self.users_in_chat.append(client_in_r)
                            logger_srv_obj.info(f'Пользователи в чате{self.users_in_chat}')
                            send_msg(client_in_r, check_client_message(new_msg))
                            logger_srv_obj.info(f'Блок информации о запросе\n'
                                                f'Тип запроса: {new_msg["action"]}\n'
                                                f'Время запроса: {utc_time.strftime("%d-%m-%Y %H:%M:%S")}\n'
                                                f'Пользователь: {new_msg["user"]}\n')
                        elif new_msg['action'] == 'message':
                            resp_to_cl = check_client_message(new_msg)
                            send_msg(client_in_r, resp_to_cl)
                            self.msg_list.append(new_msg)
                            logger_srv_obj.info(f'Блок информации о запросе\n'
                                                f'Тип запроса: {new_msg["action"]}\n'
                                                f'Время сообщения: {utc_time.strftime("%d-%m-%Y %H:%M:%S")}\n'
                                                f'Автор сообщения: {new_msg["author"]}\n'
                                                f'Текст сообщения: {new_msg["post_text"]}\n')
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
            for msg_to_send in self.msg_list:
                for user_to_send in self.users_in_chat:
                    try:
                        send_msg(user_to_send, msg_to_send)
                    except:
                        logger_srv_obj.debug('Нет соединения с клиентом')
                        self.cl_list.remove(user_to_send)
                        self.users_in_chat.remove(user_to_send)
            self.msg_list.clear()


if __name__ == '__main__':
    srv_address, serv_port = parsing_arguments()
    srv1 = Server(srv_address, serv_port)
    srv1.start_proc_srv()

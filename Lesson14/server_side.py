"""

Cерверная часть программы:
проверка аттрибутов, установка соединения,
получение сообщений, проверка и отправка сообщений клиенту

 """
import select
import sys
from datetime import datetime
from socket import *
from threading import Thread
from messageutils.check_message import check_client_message, check_msg
from messageutils.get_send_message import send_msg
import logging
import log.server_log_config
from deco_func import LogClass, login_required
from srvmeta import ServerVerifier
from descservsock import PortChecker
from db import Storage
from PyQt5.QtWidgets import QApplication, QMessageBox
from serv_admin import AdminPanel, Statistics, UsersInChat, Configuration, users_in_chat_model, statistic_model
from configparser import ConfigParser

# Создаем объект-логгер:
logger_srv_obj = logging.getLogger('app.serverside')


@LogClass()
def parsing_arguments(def_addr, def_port):
    logger_srv_obj.info('Считываем параметры адреса и порта, иначе - устанавливаем по умолчанию')
    try:
        s_address = def_addr
        s_port = def_port
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


class Server(Thread, metaclass=ServerVerifier):
    serv_port = PortChecker()

    def __init__(self, sr_address, sr_port, db):
        self.srv_address = sr_address
        self.serv_port = sr_port
        self.cl_list = []
        self.msg_list = []
        self.users_in_chat = dict()
        self.sock = None
        self.db = db
        super().__init__()

    def start_socket(self):
        logger_srv_obj.debug('Сервер запущен и ожидает входящих соединений')
        print('Сервер запущен и ожидает входящих соединений')
        serv_sock = socket(AF_INET, SOCK_STREAM)
        serv_sock.bind((self.srv_address, self.serv_port))
        serv_sock.settimeout(0.5)
        self.sock = serv_sock
        self.sock.listen()

    @login_required
    def mess_factory(self, cl_sock):
        new_msg = check_msg(cl_sock)
        utc_time = datetime.utcfromtimestamp(new_msg['time'])
        logger_srv_obj.info(f'action:{new_msg["action"]} time:{new_msg["time"]}')
        if new_msg['action'] == 'presence':
            if self.db.check_user_registration(new_msg['user']):
                if self.db.check_hash(new_msg['user'], new_msg['pass']):
                    if new_msg['user'] not in self.users_in_chat.keys():
                        self.users_in_chat[new_msg['user']] = cl_sock
                        print(f'Зарегистрирован: {new_msg["user"]}')
                        cl_ip, cl_port = cl_sock.getpeername()
                        self.db.user_login(new_msg['user'], cl_ip, cl_port, new_msg['keys'])
                        logger_srv_obj.info(f'Пользователи в чате{self.users_in_chat}')
                        send_msg(cl_sock, check_client_message(new_msg))
                        logger_srv_obj.info(f'Блок информации о запросе\n'
                                            f'Тип запроса: {new_msg["action"]}\n'
                                            f'Время запроса: {utc_time.strftime("%d-%m-%Y %H:%M:%S")}\n'
                                            f'Пользователь: {new_msg["user"]}\n')
                    else:
                        success_response = {
                            'response': 'Такой пользователь уже в чате'
                        }
                        send_msg(cl_sock, success_response)
                        self.cl_list.remove(cl_sock)
                        cl_ip, cl_port = cl_sock.getpeername()
                        print(f'Отключен клиент по адресу {cl_ip}:{cl_port}')
                        cl_sock.close()
                else:
                    success_response = {
                        'disconnect': True
                    }
                    send_msg(cl_sock, success_response)
                    self.cl_list.remove(cl_sock)
                    cl_ip, cl_port = cl_sock.getpeername()
                    print(f'Отключен клиент по адресу {cl_ip}:{cl_port}')
                    cl_sock.close()
            else:
                success_response = {
                    'response': 'Такой пользователь еще не зарегистрирован'
                }
                send_msg(cl_sock, success_response)
                self.cl_list.remove(cl_sock)
                cl_ip, cl_port = cl_sock.getpeername()
                print(f'Отключен клиент по адресу {cl_ip}:{cl_port}')
                cl_sock.close()
        elif new_msg['action'] == 'registration':
            self.db.user_registration(new_msg['user'], new_msg['ps_hsh'])
            success_response = {
                'response': 200
            }
            print(f"Создан пользователь {new_msg['user']}")
            send_msg(cl_sock, success_response)
            self.cl_list.remove(cl_sock)
            cl_sock.close()

        elif new_msg['action'] == 'message':
            if new_msg['logout']:
                self.cl_list.remove(cl_sock)
                self.db.user_logout(new_msg['author'])
                del self.users_in_chat[new_msg['author']]

            elif new_msg['post_text'] == '@active@':
                list_of_users_str = []
                all_usrs = self.db.get_users_in_chat()
                for usr in all_usrs:
                    list_of_users_str.append(usr[0])
                msg_to_send = {
                    'action': 'active',
                    'author': 'server',
                    'send_to': new_msg['author'],
                    'usrs_in_chat': list_of_users_str
                }
                self.msg_list.append(msg_to_send)
            elif new_msg['post_text'] == '@list_of_cont@':
                list_of_contacts_str = []
                contacts = self.db.get_list_connections(new_msg['author'])
                for contact in contacts:
                    list_of_contacts_str.append(contact[1])
                msg_to_send = {
                    'action': 'listcontact',
                    'author': 'server',
                    'send_to': new_msg['author'],
                    'contact_list': list_of_contacts_str
                }
                send_msg(cl_sock, msg_to_send)
            elif new_msg['post_text'] == '@list_of_users@':
                list_of_users_str = []
                users = self.db.get_all_users()
                for user in users:
                    list_of_users_str.append(user[0])
                msg_to_send = {
                    'action': 'listusers',
                    'author': 'server',
                    'send_to': new_msg['author'],
                    'users_list': list_of_users_str
                }
                send_msg(cl_sock, msg_to_send)
            elif new_msg['post_text'] == '@logins@':
                all_logins_list = []
                all_logins = self.db.get_list_logins(new_msg['author'])
                for login in all_logins:
                    all_logins_list.append(login[1:])
                msg_to_send = {
                    'action': 'logins',
                    'author': 'server',
                    'send_to': new_msg['author'],
                    'post_text': str(all_logins_list),
                }
                self.msg_list.append(msg_to_send)
            elif new_msg['post_text'] == '@contact@':
                list_of_contacts_str = []
                contacts = self.db.get_list_connections(new_msg['author'])
                for contact in contacts:
                    list_of_contacts_str.append(contact[1])
                msg_to_send = {
                    'action': 'contact',
                    'author': 'server',
                    'send_to': new_msg['author'],
                    'post_text': str(list_of_contacts_str),
                }
                self.msg_list.append(msg_to_send)
            elif new_msg['post_text'] == '@create@':
                self.db.make_contact(new_msg['author'], new_msg['send_to'])
                success_response = {
                    'response': 200
                }
                send_msg(cl_sock, success_response)
            elif new_msg['post_text'] == '@pub_key@':
                key2 = self.db.get_pubkey(new_msg['send_to'])
                success_response = {
                    'pub_key': key2
                }
                send_msg(cl_sock, success_response)
            elif new_msg['post_text'] == '@delete@':
                self.db.delete_contact(new_msg['author'], new_msg['send_to'])
                success_response = {
                    'response': 200
                }
                send_msg(cl_sock, success_response)
            else:
                self.db.make_contact(new_msg['author'], new_msg['send_to'])
                resp_to_cl = check_client_message(new_msg)
                send_msg(cl_sock, resp_to_cl)
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
            send_msg(cl_sock, bad_response)

    def run(self):
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
                        self.mess_factory(client_in_r)
                    except:
                        pass
                        # logger_srv_obj.debug(f'Нет соединения с клиентом {client_in_r}')
                        # cl_list.remove(client_in_r)
            for msg_to_send in self.msg_list:
                usr = msg_to_send['send_to']
                try:
                    user_to_send = self.users_in_chat[usr]
                except KeyError:
                    user_to_send = self.users_in_chat[msg_to_send['author']]
                    warn = f'Пользователь {usr} уже не в сети'
                    msg_to_send = {
                        'action': 'message',
                        'author': 'server',
                        'send_to': msg_to_send['author'],
                        'post_text': warn,
                    }
                try:
                    send_msg(user_to_send, msg_to_send)
                except:
                    logger_srv_obj.debug('Нет соединения с клиентом')
                    self.cl_list.remove(user_to_send)
                    del self.users_in_chat[usr]
            self.msg_list.clear()


def start_serv():
    def make_config_file(conf_obj):
        serv_name = input('Введите наименование сервера  ')
        add = input('Введите адрес сервера по умолчанию  ')
        port = input('Введите порт сервера по умолчанию  ')
        conf_obj["Variables"] = {
            "Database_name": serv_name,
            "Default_address": add,
            "Default_port": int(port),
        }
        with open("srv_config.ini", "w") as file_object:
            conf_obj.write(file_object)

    def server_config():
        global cfg_field
        cfg_field = Configuration()
        cfg_field.db_name.insert(config['Variables']['Database_name'])
        cfg_field.ip.insert(config['Variables']['Default_address'])
        cfg_field.port.insert(config['Variables']['Default_port'])
        cfg_field.save_btn.clicked.connect(save_server_config)

    def save_server_config():
        global cfg_field
        message = QMessageBox()
        config['Variables']['Database_name'] = cfg_field.db_name.text()
        config['Variables']['Default_address'] = cfg_field.ip.text()
        config['Variables']['Default_port'] = cfg_field.port.text()
        with open('srv_config.ini', 'w') as srv_config:
            config.write(srv_config)
            message.information(
                cfg_field, 'OK', 'Настройки сохранены!')

    config = ConfigParser()
    try:
        config.read('srv_config.ini')
        srv_address, serv_port = parsing_arguments(config['Variables']['Default_address'],
                                                   config['Variables']['Default_port'],
                                                   )
    except KeyError:
        make_config_file(config)
        srv_address, serv_port = parsing_arguments(config['Variables']['Default_address'],
                                                   config['Variables']['Default_port'],
                                                   )
    db1 = Storage(config['Variables']['Database_name'])
    srv1 = Server(srv_address, serv_port, db1)
    srv1.daemon = True
    srv1.start()
    server_app = QApplication(sys.argv)
    admin_ui = AdminPanel()

    admin_ui.statusBar().showMessage('Сервер запущен')

    def show_statistics():
        global stat_field
        stat_field = Statistics()
        user_stat = admin_ui.user.text()
        if len(user_stat) > 0:
            stat_field.logins_table.setModel(statistic_model(db1, user_stat))
        else:
            n = 'all'
            stat_field.logins_table.setModel(statistic_model(db1, n))
        stat_field.logins_table.resizeColumnsToContents()
        stat_field.logins_table.resizeRowsToContents()
        stat_field.show()

    def show_users_in_chat():
        global users_field
        users_field = UsersInChat()
        users_field.chatusers_table.setModel(users_in_chat_model(db1))
        users_field.chatusers_table.resizeColumnsToContents()
        users_field.chatusers_table.resizeRowsToContents()
        users_field.show()

    admin_ui.usersbtn.triggered.connect(show_users_in_chat)
    admin_ui.user_stats_button.triggered.connect(show_statistics)
    admin_ui.config_btn.triggered.connect(server_config)
    server_app.exec_()


if __name__ == '__main__':
    start_serv()

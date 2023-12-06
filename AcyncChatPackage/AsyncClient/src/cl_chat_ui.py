import base64
import hashlib
import json
from socket import socket, AF_INET, SOCK_STREAM
from time import time, sleep

from Crypto.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QApplication, QLabel, QMainWindow, QMessageBox, \
    QComboBox

from messageutils.check_message import check_msg
from messageutils.get_send_message import send_msg
from template_chat import UiMainClientWindow


class InputUserName(QDialog):
    def __init__(self, server_address, server_port):
        super().__init__()
        self.approved = False
        self.registration = False
        self.serv = server_address
        self.port = server_port
        self.setWindowTitle('Панель входа в чат')
        self.setFixedSize(450, 190)
        self.username_label = QLabel('Введите имя для чата:', self)
        self.username_label.move(10, 10)
        self.username_label.setFixedSize(150, 20)
        self.username = QLineEdit(self)
        self.username.setFixedSize(154, 20)
        self.username.move(10, 30)
        self.passwd_label = QLabel('Введите пароль:', self)
        self.passwd_label.move(230, 10)
        self.passwd_label.setFixedSize(150, 20)
        self.passwd = QLineEdit(self)
        self.passwd.setEchoMode(QLineEdit.Password)
        self.passwd.setFixedSize(154, 20)
        self.passwd.move(230, 40)
        self.btn_approved = QPushButton('Войти в чат', self)
        self.btn_approved.move(10, 60)
        self.btn_approved.setFixedSize(150, 30)
        self.btn_approved.clicked.connect(self.aprove)
        self.btn_registration = QPushButton('Регистрация', self)
        self.btn_registration.move(10, 90)
        self.btn_registration.setFixedSize(150, 30)
        self.btn_registration.clicked.connect(self.regist)
        self.btn_decl = QPushButton('Отмена', self)
        self.btn_decl.move(10, 150)
        self.btn_decl.setFixedSize(150, 30)
        self.btn_decl.clicked.connect(self.closewind)
        self.show()

    def aprove(self):
        self.approved = True
        self.close()

    def regist(self):
        global regist_dialog
        regist_dialog = RegisterDialog(self.serv, self.port)
        regist_dialog.show()

    def closewind(self):
        self.close()


class RegisterDialog(QDialog):
    def __init__(self, ser, por):
        super().__init__()
        self.server = ser
        self.port = por
        self.regmessages = QMessageBox()
        self.setFixedSize(450, 200)
        self.setWindowTitle('Регистрация нового пользователя')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.new_usr_label = QLabel('Введите имя для регистрации:', self)
        self.new_usr_label.move(10, 10)
        self.new_usr_label.setFixedSize(220, 20)
        self.new_usr = QLineEdit(self)
        self.new_usr.setFixedSize(154, 20)
        self.new_usr.move(10, 40)
        self.passw_label = QLabel('Введите пароль:', self)
        self.passw_label.move(230, 10)
        self.passw_label.setFixedSize(150, 20)
        self.passw = QLineEdit(self)
        self.passw.setEchoMode(QLineEdit.Password)
        self.passw.setFixedSize(154, 20)
        self.passw.move(230, 40)
        self.passw2_label = QLabel('Подтвердите пароль:', self)
        self.passw2_label.move(230, 70)
        self.passw2_label.setFixedSize(150, 20)
        self.passw2 = QLineEdit(self)
        self.passw2.setEchoMode(QLineEdit.Password)
        self.passw2.setFixedSize(154, 20)
        self.passw2.move(230, 90)
        self.passw_msg_label = QLabel('', self)
        self.passw_msg_label.move(230, 120)
        self.passw_msg_label.setFixedSize(200, 20)
        self.btn_regist = QPushButton('Зарегистрироваться', self)
        self.btn_regist.setFixedSize(154, 30)
        self.btn_regist.move(20, 140)
        self.btn_regist.clicked.connect(self.send_regist)
        self.btn_cancel = QPushButton('Отмена', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(200, 140)
        self.btn_cancel.clicked.connect(self.closewind2)

    def send_regist(self):
        self.passw_msg_label.setText('')
        pass1 = self.passw.text()
        pass2 = self.passw2.text()
        user = self.new_usr.text()
        if pass1 != pass2:
            self.passw_msg_label.setText(f'Пароли должны совпадать!')
        else:
            self.passw_msg_label.setText('')
            new_socket = socket(AF_INET, SOCK_STREAM)
            new_socket.connect((self.server, self.port))
            hash_to_send = self.generate_hash(pass1)
            request33 = {
                'action': 'registration',
                'user': user,
                'time': time(),
                'ps_hsh': hash_to_send
            }
            send_msg(new_socket, request33)
            serv_answer3 = check_msg(new_socket)
            if serv_answer3['response'] == 200:
                self.regmessages.information(self, 'Статус', 'Пользователь успешно добавлен.')
                sleep(3)
                self.close()

    def generate_hash(self, pass_to_hash):
        passwd_bt = pass_to_hash.encode('utf-8')
        to_salt = 'simple_salt'
        salt = to_salt.encode('utf-8')
        passwd_hash = hashlib.pbkdf2_hmac('sha512', passwd_bt, salt, 1000)
        passwd_hash_str = passwd_hash.hex()
        return passwd_hash_str

    def closewind2(self):
        self.close()


class AddContactDialog(QDialog):
    def __init__(self, transport, database, user):
        super().__init__()
        self.transport = transport
        self.database = database
        self.user = user
        self.setFixedSize(350, 120)
        self.setWindowTitle('Запуск нового чата')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)
        self.selector_label = QLabel('Начать чат с пользователем:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)
        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)
        self.btn_refresh = QPushButton('Получить список \n пользователей', self)
        self.btn_refresh.setFixedSize(200, 55)
        self.btn_refresh.move(10, 60)
        self.btn_ok = QPushButton('Добавить', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)
        self.btn_cancel = QPushButton('Отмена', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.closewind3)
        self.btn_refresh.clicked.connect(self.get_my_contacts)

    def get_my_contacts(self):
        self.selector.clear()
        contacts_list = set(self.database.get_contacts())
        users_list = set(self.transport.get_users_from_server(self.user))
        users_list.remove(self.transport.username)
        self.selector.addItems(users_list - contacts_list)

    def closewind3(self):
        self.close()


class DelContactDialog(QDialog):
    def __init__(self, database):
        super().__init__()
        self.database = database
        self.setFixedSize(350, 120)
        self.setWindowTitle('Удаление чата')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)
        self.selector_label = QLabel('Удалить чат с пользователем:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)
        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)
        self.btn_ok = QPushButton('Удалить', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)
        self.btn_cancel = QPushButton('Отмена', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.closewind4)
        self.selector.addItems(sorted(self.database.get_contacts()))

    def closewind4(self):
        self.close()


class ClientMainWindow(QMainWindow):
    def __init__(self, database, transport, chat_user, keys):
        super().__init__()
        self.database = database
        self.transport = transport
        self.chat_user = chat_user
        self.decrypter = PKCS1_OAEP.new(keys)
        self.encryptor = None
        self.ui = UiMainClientWindow()
        self.ui.setupui(self)
        self.ui.btn_send.clicked.connect(self.send_message)
        self.ui.btn_add_contact.clicked.connect(self.add_contact_window)
        self.ui.btn_remove_contact.clicked.connect(self.delete_contact_window)
        self.contacts_model = None
        self.history_model = None
        self.messages = QMessageBox()
        self.current_chat = None
        self.current_chat_key = None
        self.ui.list_messages.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.list_messages.setWordWrap(True)
        self.ui.list_contacts.doubleClicked.connect(self.select_active_user)
        self.clients_list_update()
        self.set_disabled_input()
        self.show()

    def set_disabled_input(self):
        self.ui.label_new_message.setText('Выберите получателя сообщения ------------------------------------->')
        self.ui.text_message.clear()
        if self.history_model:
            self.history_model.clear()
        self.ui.btn_clear.setDisabled(True)
        self.ui.btn_send.setDisabled(True)
        self.ui.text_message.setDisabled(True)
        self.ui.statusBar.showMessage('Не выбран чат для переписки')

    def history_list_update(self):
        hist_list = sorted(self.database.get_message_from_db(self.current_chat), key=lambda item: item[3])
        if not self.history_model:
            self.history_model = QStandardItemModel()
            self.ui.list_messages.setModel(self.history_model)
        self.history_model.clear()
        length = len(hist_list)
        start_index = 0
        if length > 25:
            start_index = length - 25
        for i in range(start_index, length):
            item = hist_list[i]
            if item[1]:
                mess = QStandardItem(f'{item[0]}({item[3].replace(microsecond=0)}):\n {item[2]}')
                mess.setEditable(False)
                mess.setBackground(QBrush(QColor(255, 213, 213)))
                mess.setTextAlignment(Qt.AlignLeft)
                self.history_model.appendRow(mess)
            else:
                mess = QStandardItem(f'Вы({item[3].replace(microsecond=0)}):\n {item[2]}')
                mess.setEditable(False)
                mess.setTextAlignment(Qt.AlignRight)
                mess.setBackground(QBrush(QColor(204, 255, 204)))
                self.history_model.appendRow(mess)
        self.ui.list_messages.scrollToBottom()

    def select_active_user(self):
        self.current_chat = self.ui.list_contacts.currentIndex().data()
        self.set_active_user()

    def set_active_user(self):
        try:
            self.current_chat_key = self.transport.get_p_key(self.current_chat)
            print(f'Загружен открытый ключ для {self.current_chat}')
            if self.current_chat_key:
                self.encryptor = PKCS1_OAEP.new(RSA.import_key(self.current_chat_key))
        except (OSError, json.JSONDecodeError):
            self.current_chat_key = None
            self.encryptor = None

        if not self.current_chat_key:
            self.messages.warning(
                self, 'Ошибка', 'Для выбранного пользователя нет ключа шифрования.')
            return
        self.ui.label_new_message.setText(f'Введите сообщенние для {self.current_chat}:')
        self.ui.statusBar.showMessage(f'Запущен чат с пользователем {self.current_chat}')
        self.ui.btn_clear.setDisabled(False)
        self.ui.btn_send.setDisabled(False)
        self.ui.text_message.setDisabled(False)
        self.history_list_update()

    def set_inactive_user(self):
        self.ui.label_new_message.setText(f'Пользователь {self.current_chat} '
                                          f'не в сети, отправка сообщений не возможна')
        self.ui.btn_clear.setDisabled(False)
        self.ui.btn_send.setDisabled(True)
        self.ui.text_message.setDisabled(False)

        self.encryptor = None
        self.current_chat = None
        self.current_chat_key = None

    def clients_list_update(self):
        contacts_list = self.database.get_contacts()
        self.contacts_model = QStandardItemModel()
        for i in sorted(contacts_list):
            item = QStandardItem(i)
            item.setEditable(False)
            self.contacts_model.appendRow(item)
        self.ui.list_contacts.setModel(self.contacts_model)

    def add_contact_window(self):
        global select_dialog
        select_dialog = AddContactDialog(self.transport, self.database, self.chat_user)
        select_dialog.btn_ok.clicked.connect(lambda: self.add_contact_action(select_dialog))
        select_dialog.show()

    def add_contact_action(self, item):
        new_contact = item.selector.currentText()
        self.add_contact(new_contact)
        item.close()

    def add_contact(self, new_contact):
        self.transport.add_contact(new_contact)
        self.database.add_contact(new_contact)
        new_contact = QStandardItem(new_contact)
        new_contact.setEditable(False)
        self.contacts_model.appendRow(new_contact)
        self.messages.information(self, 'Статус', 'Чат успешно добавлен.')

    def delete_contact_window(self):
        global remove_dialog
        remove_dialog = DelContactDialog(self.database)
        remove_dialog.btn_ok.clicked.connect(lambda: self.delete_contact(remove_dialog))
        remove_dialog.show()

    def delete_contact(self, item):
        selected = item.selector.currentText()
        self.transport.delete_contact(selected)
        self.database.del_contact(selected)
        self.clients_list_update()
        self.messages.information(self, 'Статус', 'Чат успешно удалён.')
        item.close()
        if selected == self.current_chat:
            self.current_chat = None
            self.set_disabled_input()

    def send_message(self):
        message_text = self.ui.text_message.toPlainText()
        self.ui.text_message.clear()
        if not message_text:
            return

        msg_enc = self.encryptor.encrypt(
            message_text.encode('utf8'))
        msg_enc_base64 = base64.b64encode(
            msg_enc)
        try:
            self.transport.send_message(self.current_chat, msg_enc_base64.decode('ascii'))
            pass
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Ошибка', 'Потеряно соединение с сервером!')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        except (ConnectionResetError, ConnectionAbortedError):
            self.messages.critical(self, 'Ошибка', 'Потеряно соединение с сервером!')
            self.close()
        else:
            self.database.store_message_in_db(self.current_chat, False, message_text)
            self.history_list_update()

    @pyqtSlot(dict)
    def message(self, message):
        encryp_message = base64.b64decode(message['post_text'])
        try:
            decryp_message = self.decrypter.decrypt(encryp_message)
        except (ValueError, TypeError):
            self.messages.warning(
                self, 'Ошибка', 'Не удалось декодировать сообщение.')
            return
        self.database.store_message_in_db(self.current_chat, True,
                                          decryp_message.decode('utf8'))
        sender = message['author']
        if sender == self.current_chat:
            self.history_list_update()
        else:
            if self.database.check_contact(sender):
                if self.messages.question(self, 'Новое сообщение',
                                          f'Получено сообщение от {sender}. Открыть чат с ним?', QMessageBox.Yes,
                                          QMessageBox.No) == QMessageBox.Yes:
                    self.current_chat = sender
                    self.set_active_user()
            else:
                if self.messages.question(self, 'Новое сообщение',
                                          f'Получено новое сообщение от {sender}.\n Данного пользователя нет в вашем'
                                          f' списке чатов.\n Открыть новый чат?',
                                          QMessageBox.Yes,
                                          QMessageBox.No) == QMessageBox.Yes:
                    print("111")
                    self.add_contact(sender)
                    print("222")
                    self.current_chat = sender
                    self.set_active_user()

    @pyqtSlot()
    def connection_lost(self):
        self.messages.warning(self, 'Сбой соединения', 'Потеряно соединение с сервером. ')
        self.close()

    def make_connection(self, trans_obj):
        trans_obj.new_message.connect(self.message)
        trans_obj.connection_lost.connect(self.connection_lost)


if __name__ == '__main__':
    app = QApplication([])
    app.exec_()

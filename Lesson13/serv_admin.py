import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QLabel, QTableView, QDialog, QPushButton, \
    QLineEdit, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt



def users_in_chat_model(srvdb):
    list_users = srvdb.get_users_in_chat()
    usrs = QStandardItemModel()
    usrs.setHorizontalHeaderLabels(['Пользователь', 'Время входа'])
    for row in list_users:
        user, time = row
        user = QStandardItem(user)
        user.setEditable(False)
        time = QStandardItem(time)
        time.setEditable(False)
        usrs.appendRow([user, time])
    return usrs


def statistic_model(srvdb, user):
    logins_lst = srvdb.get_list_logins(user)
    logins = QStandardItemModel()
    logins.setHorizontalHeaderLabels(
        ['Пользователь', 'Время входа', 'IP-адрес'])
    for data in logins_lst:
        user, time, ip = data
        user = QStandardItem(user)
        user.setEditable(False)
        time = QStandardItem(time)
        time.setEditable(False)
        ip = QStandardItem(ip)
        ip.setEditable(False)
        logins.appendRow([user, time, ip])
    return logins


class AdminPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        exitAction = QAction('Выход', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)
        self.usersbtn = QAction('Пользователи в чате', self)
        self.config_btn = QAction('Настройки сервера', self)
        self.user_stats_button = QAction('Статистика клиентов', self)
        self.statusBar()
        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(self.usersbtn)
        self.toolbar.addAction(self.user_stats_button)
        self.toolbar.addAction(self.config_btn)
        self.setFixedSize(450, 150)
        self.setWindowTitle('Административная панель сервера')
        self.user_label = QLabel(f'Имя пользователя для статистики \n '
                                 f'(оставьте пустым для статистики по всем пользователям): ', self)
        self.user_label.move(10, 30)
        self.user_label.setFixedSize(450 , 30)
        self.user = QLineEdit(self)
        self.user.setFixedSize(250, 20)
        self.user.move(10, 70)
        self.show()


class Statistics(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Статистика пользователей')
        self.setFixedSize(500, 500)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.close_button = QPushButton('Закрыть', self)
        self.close_button.move(215, 450)
        self.close_button.clicked.connect(self.close)
        self.logins_table = QTableView(self)
        self.logins_table.move(10, 10)
        self.logins_table.setFixedSize(480, 400)
        self.show()

class UsersInChat(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Пользователи в чате')
        self.setFixedSize(500, 500)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.close_button = QPushButton('Закрыть', self)
        self.close_button.move(215, 450)
        self.close_button.clicked.connect(self.close)

        self.chatusers_table = QTableView(self)
        self.chatusers_table.move(10, 10)
        self.chatusers_table.setFixedSize(480, 400)

        self.show()


class Configuration(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(365, 260)
        self.setWindowTitle('Настройки сервера')

        self.db_name_label = QLabel('Наименование базы данных: ', self)
        self.db_name_label.move(10, 10)
        self.db_name_label.setFixedSize(250 , 20)

        self.db_name = QLineEdit(self)
        self.db_name.setFixedSize(250, 20)
        self.db_name.move(10, 30)

        self.ip_label = QLabel('Адрес сервера по умолчанию:', self)
        self.ip_label.move(10, 108)
        self.ip_label.setFixedSize(200, 20)

        self.ip = QLineEdit(self)
        self.ip.move(210, 108)
        self.ip.setFixedSize(150, 20)

        self.port_label = QLabel('Порт по умолчанию:', self)
        self.port_label.move(10, 148)
        self.port_label.setFixedSize(180, 15)

        self.port = QLineEdit(self)
        self.port.move(210, 148)
        self.port.setFixedSize(150, 20)


        self.save_btn = QPushButton('Сохранить' , self)
        self.save_btn.move(100, 220)

        self.close_button = QPushButton('Закрыть', self)
        self.close_button.move(255, 220)
        self.close_button.clicked.connect(self.close)

        self.show()


if __name__ == '__main__':
    test_app = QApplication(sys.argv)
    test_message = QMessageBox
    test_conf = Configuration()
    test_app.exec_()
from PyQt5 import QtCore, QtWidgets


class UiMainClientWindow(object):
    def setupui(self, MainClientWindow):
        MainClientWindow.setObjectName("MainClientWindow")
        MainClientWindow.resize(756, 534)
        MainClientWindow.setMinimumSize(QtCore.QSize(756, 534))
        self.centralwidget = QtWidgets.QWidget(MainClientWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_contacts = QtWidgets.QLabel(self.centralwidget)
        self.label_contacts.setGeometry(QtCore.QRect(495, 5, 101, 16))
        self.label_contacts.setObjectName("label_contacts")
        self.btn_add_contact = QtWidgets.QPushButton(self.centralwidget)
        self.btn_add_contact.setGeometry(QtCore.QRect(495, 440, 251, 30))
        self.btn_add_contact.setObjectName("btn_add_contact")
        self.btn_remove_contact = QtWidgets.QPushButton(self.centralwidget)
        self.btn_remove_contact.setGeometry(QtCore.QRect(495, 470, 251, 30))
        self.btn_remove_contact.setObjectName("btn_remove_contact")
        self.label_history = QtWidgets.QLabel(self.centralwidget)
        self.label_history.setGeometry(QtCore.QRect(10, 5, 391, 21))
        self.label_history.setObjectName("label_history")
        self.text_message = QtWidgets.QTextEdit(self.centralwidget)
        self.text_message.setGeometry(QtCore.QRect(10, 360, 321, 140))
        self.text_message.setObjectName("text_message")
        self.label_new_message = QtWidgets.QLabel(self.centralwidget)
        self.label_new_message.setGeometry(QtCore.QRect(10, 335, 450, 16))  # Правка тут
        self.label_new_message.setObjectName("label_new_message")
        self.list_contacts = QtWidgets.QListView(self.centralwidget)
        self.list_contacts.setGeometry(QtCore.QRect(495, 25, 251, 411))
        self.list_contacts.setObjectName("list_contacts")
        self.list_messages = QtWidgets.QListView(self.centralwidget)
        self.list_messages.setGeometry(QtCore.QRect(10, 25, 441, 301))
        self.list_messages.setObjectName("list_messages")
        self.btn_send = QtWidgets.QPushButton(self.centralwidget)
        self.btn_send.setGeometry(QtCore.QRect(330, 440, 130, 30))
        self.btn_send.setObjectName("btn_send")
        self.btn_clear = QtWidgets.QPushButton(self.centralwidget)
        self.btn_clear.setGeometry(QtCore.QRect(330, 470, 130, 30))
        self.btn_clear.setObjectName("btn_clear")
        MainClientWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainClientWindow)
        self.statusBar.setObjectName("statusBar")
        MainClientWindow.setStatusBar(self.statusBar)
        self.retranslateui(MainClientWindow)
        self.btn_clear.clicked.connect(self.text_message.clear)
        QtCore.QMetaObject.connectSlotsByName(MainClientWindow)

    def retranslateui(self, MainClientWindow):
        _translate = QtCore.QCoreApplication.translate
        MainClientWindow.setWindowTitle(_translate("MainClientWindow", "Асинхронный чат"))
        self.label_contacts.setText(_translate("MainClientWindow", "Ваши чаты:"))
        self.btn_add_contact.setText(_translate("MainClientWindow", "Начать новый чат"))
        self.btn_remove_contact.setText(_translate("MainClientWindow", "Удалить чат"))
        self.label_history.setText(_translate("MainClientWindow", "Окно сообщений:"))
        self.label_new_message.setText(_translate("MainClientWindow", "Введите сообщение:"))
        self.btn_send.setText(_translate("MainClientWindow", "Отправить"))
        self.btn_clear.setText(_translate("MainClientWindow", "Очистить"))

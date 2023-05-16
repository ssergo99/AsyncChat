import time
import os
from subprocess import Popen

USER_INTER_VAR = """
Для выбора действия введите одно из следующих значений: 
Запустить сервер - s
Остановить сервер - x
Запустить [Х] пар клиентов (пара = 1 читающий, 1 пишуший) - Х->число пар
Остановить всех клиентов - y
Остановить сервер иклиентов и выйти - q


 """

clients = []
server = ''
PATH_TO_FILE = os.path.dirname(__file__)
PATH_TO_SERVER_SCRIPT = os.path.join(PATH_TO_FILE, "server_side.py")
PATH_TO_CLIENT_SCRIPT = os.path.join(PATH_TO_FILE, "client_side.py")

while True:
    user_choice = input(USER_INTER_VAR)

    if user_choice == 's':
        server = Popen(
            f'osascript -e \'tell application "Terminal" to do'
            f' script "python {PATH_TO_SERVER_SCRIPT}"\'', shell=True)
    elif user_choice == 'x':
        server.kill()
    elif user_choice.isnumeric():
        for i in range(int(user_choice)):
            clients.append(
                Popen(
                    f'osascript -e \'tell application "Terminal" to do'
                    f' script "python {PATH_TO_CLIENT_SCRIPT} 127.0.0.1 7777"\'', shell=True))
            clients.append(
                Popen(
                    f'osascript -e \'tell application "Terminal" to do'
                    f' script "python {PATH_TO_CLIENT_SCRIPT} 127.0.0.1 7777 snd"\'', shell=True))
            time.sleep(0.5)
    elif user_choice == 'y':
        for i in range(len(clients)):
            clients[i].kill()
    elif user_choice == 'q':
        for i in range(len(clients)):
            clients[i].kill()
        server.kill()
        break

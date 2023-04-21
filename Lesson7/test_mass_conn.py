from subprocess import Popen, CREATE_NEW_CONSOLE
import logging
import log.server_log_config
import log.client_log_config

logger_srv_obj = logging.getLogger('app.serverside')
logger_cl_obj = logging.getLogger('app.clientside')

proc_list = []
while True:
    user_act = input("Запустить 1 сервер, 3 отправляющих клиента и 3 принимающих клиента (s) / Закрыть сервер и "
                     "клиентов (x) / Выйти (q) ")
    if user_act == 'q':
        break
    elif user_act == 's':
        proc_list.append(Popen('python server_side.py -a 127.0.0.1 -p 9999', shell=True,
                               creationflags=CREATE_NEW_CONSOLE))
        logger_srv_obj.debug(f'Запущен сервер по адресу 127.0.0.1 Порт: 9999')
        for i in range(3):
            proc_list.append(Popen('python client_side.py 127.0.0.1 9999 snd', shell=True,
                                   creationflags=CREATE_NEW_CONSOLE))
        logger_cl_obj.debug(f'Запущено 3 отправляющих клиента')
        for i in range(3):
            proc_list.append(Popen('python client_side.py 127.0.0.1 9999 rcv', shell=True,
                                   creationflags=CREATE_NEW_CONSOLE))
        logger_cl_obj.debug(f'Запущено 3 принимающих клиента')
    elif user_act == 'x':
        for proc in proc_list:
            proc.kill()
        proc_list.clear()

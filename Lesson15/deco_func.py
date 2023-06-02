import inspect
import logging

import log.server_log_config
import log.client_log_config
from socket import *


class LogClass:
    """Класс-декоратор"""

    def __call__(self, st_func):
        def logging_func(*args, **kwargs):
            req_func_cl = inspect.stack()[1][3]
            if req_func_cl == '<module>':
                req_func_txt = f'модуля {st_func.__module__}'
                if inspect.getfile(st_func).split("/")[-1] == 'client_side.py':
                    logger = logging.getLogger('app.clientside')
                else:
                    logger = logging.getLogger('app.serverside')
            else:
                req_func_txt = f'функции {inspect.stack()[1][3]}'
                if inspect.stack()[1][3] == 'start_proc_srv':
                    logger = logging.getLogger('app.serverside')
                else:
                    logger = logging.getLogger('app.clientside')
            logger.debug(f'Функция {st_func.__name__}, '
                         f'позиционные аргументы: {args}, именованные аргументы: {kwargs}.')
            logger.debug(f'Функция {st_func.__name__} вызвана из '
                         f'{req_func_txt}.')

            res = st_func(*args, **kwargs)
            return res

        return logging_func


def login_required(func):
    def check_auth(*args, **kwargs):
        from server_side import Server
        if isinstance(args[0], Server):
            login_index = False
            for arg in args:
                if isinstance(arg, socket):
                    for client in args[0].users_in_chat:
                        if args[0].users_in_chat[client] == arg:
                            login_index = True
            for arg in args:
                if isinstance(arg, dict):
                    if 'action' in arg and arg['action'] == 'presence':
                        login_index = True
            if not login_index:
                raise TypeError
        return func(*args, **kwargs)

    return check_auth

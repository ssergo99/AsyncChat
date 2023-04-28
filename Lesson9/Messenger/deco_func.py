import inspect
import logging

import log.server_log_config
import log.client_log_config


def log(start_func):
    """

    Описываем декоратор, фиксирующий в логе
    исполняемую функцию(задекорированную) и функцию ее вызвавшую

    """
    def logging_func(*args, **kwargs):

        req_func = inspect.stack()[1][3]
        if req_func == '<module>':
            req_func_text = f'модуля {start_func.__module__}'
            if inspect.getfile(start_func).split("/")[-1] == 'client_side.py':
                logger = logging.getLogger('app.clientside')
            else:
                logger = logging.getLogger('app.serverside')
        else:
            req_func_text = f'функции {inspect.stack()[1][3]}'
            if inspect.stack()[1][3] == 'start_proc_srv':
                logger = logging.getLogger('app.serverside')
            else:
                logger = logging.getLogger('app.clientside')
        logger.debug(f'Функция {start_func.__name__}, '
                            f'позиционные аргументы: {args}, именованные аргументы: {kwargs}.')
        logger.debug(f'Функция {start_func.__name__} вызвана из '
                            f'{req_func_text}.')

        result = start_func(*args, **kwargs)

        return result

    return logging_func
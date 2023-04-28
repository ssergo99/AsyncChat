import inspect
import logging

import log.server_log_config
import log.client_log_config


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

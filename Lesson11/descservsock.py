import logging

logger_srv_obj = logging.getLogger('app.serverside')


class PortChecker:
    def __set__(self, instance, value):
        try:
            if value.isnumeric() and int(value) < 65534:
                instance.__dict__['serv_port'] = int(value)
            else:
                logger_srv_obj.info('Некорректный номер порта. Установлено значение по умолчанию.')
                instance.__dict__['serv_port'] = 7777
        except AttributeError:
            logger_srv_obj.info('Некорректный номер порта. Установлено значение по умолчанию.')
            instance.__dict__['serv_port'] = 7777
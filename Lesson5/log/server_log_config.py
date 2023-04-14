"""

Создание логгера на серверной стороне

"""

import logging.handlers
import logging

# Создаем объект-логгер с именем app.serverside:
logger_srv = logging.getLogger('app.serverside')

# Создаем объект форматирования:
formatter_srv = logging.Formatter('Дата-время: %(asctime)s Уровень важности: %(levelname)s Имя модуля: %(filename)s '
                                  'Сообщение: %(message)s')

# Создаем файловый обработчик логирования:
filehandler_srv = logging.handlers.TimedRotatingFileHandler("app.serverside.log", when='D', interval=1,
                                                            encoding='utf-8')
filehandler_srv.setLevel(logging.DEBUG)
filehandler_srv.setFormatter(formatter_srv)

# Добавляем в логгер новый обработчик событий и устанавливаем уровень логирования:
logger_srv.addHandler(filehandler_srv)
logger_srv.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # Запуск логирования:
    logger_srv.info('Тестовый запуск логирования')


"""

Создание логгера на клиентской стороне

"""

import logging

# Создаем объект-логгер с именем app.clientside:
logger_cl = logging.getLogger('app.clientside')

# Создаем объект форматирования:
formatter_cl = logging.Formatter('Дата-время: %(asctime)s %(message)s')

# Создаем файловый обработчик логирования:
filehandler_cl = logging.FileHandler("app.clientside.log", encoding='utf-8')
filehandler_cl.setLevel(logging.DEBUG)
filehandler_cl.setFormatter(formatter_cl)

# Добавляем в логгер новый обработчик событий и устанавливаем уровень логирования:
logger_cl.addHandler(filehandler_cl)
logger_cl.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # Запуск логирования:
    logger_cl.info('Тестовый запуск логирования')


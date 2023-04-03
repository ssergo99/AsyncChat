"""

5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

"""

import subprocess
import chardet


def ping_encode(url_str):
    args = ['ping', url_str]
    url_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in url_ping.stdout:
        detect_encode = chardet.detect(line)['encoding']
        print(detect_encode)
        line = line.decode(detect_encode).encode('utf-8')
        print(line.decode('utf-8'))


# 1) Для yandex.ru:
ping_encode('yandex.ru')
# 2) Для youtube.com:
ping_encode('youtube.com')

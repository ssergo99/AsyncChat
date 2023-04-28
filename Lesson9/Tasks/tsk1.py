"""

Написать функцию host_ping(), в которой с помощью утилиты ping будет
проверяться доступность сетевых узлов. Аргументом функции является список,
в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять их доступность с выводом
соответствующего сообщения («Узел доступен», «Узел недоступен»).
При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().

"""

from subprocess import Popen, PIPE
from ipaddress import ip_address
import socket


def host_ping(list_of_hosts, only_sum=None):
    summary = {'Reachable': "", 'Unreachable': ""}
    for host in list_of_hosts:
        ip_host = ip_address('127.0.0.1')
        name = 'no name'
        try:
            ip_host = ip_address(host)
            name = '<<<'
        except ValueError:
            host_to_convert = socket.gethostbyname(host)
            ip_host = ip_address(host_to_convert)
            name = host + ' <<<'
        finally:
            test_ping = Popen(['ping', str(ip_host), '-c 1'], shell=False, stdout=PIPE)
            test_ping.wait()
            if test_ping.returncode == 0:
                if not only_sum:
                    print(f'Узел {ip_host} {name} доступен')
                summary['Reachable'] += f'{str(ip_host)}\n'
            else:
                if not only_sum:
                    print(f'Узел {ip_host} {name} не доступен')
                summary['Unreachable'] += f'{str(ip_host)}\n'
    return summary


if __name__ == '__main__':
    sample_host_list = ['yandex.ru', 'linkedin.com', '77.0.0.12', '192.168.0.5', '127.0.0.1', 'google.com']
    host_ping(sample_host_list)

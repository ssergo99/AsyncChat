"""

Написать функцию host_range_ping() для перебора ip-адресов из
заданного диапазона. Меняться должен только последний октет каждого адреса.
По результатам проверки должно выводиться соответствующее сообщение.

"""

from ipaddress import ip_address
from tsk1 import host_ping


def host_range_ping(only_sum=None):
    sample_host_list = []
    range_ip_start = input('Укажите адрес начала диапазона: ')
    lastoct_ip_start = int(range_ip_start.split('.')[3])
    range_ip_qty = int(input('Введите количество адресов для проверки: '))
    lastoct_ip_end = lastoct_ip_start + range_ip_qty
    if lastoct_ip_end <= 254:
        for i in range(range_ip_qty):
            sample_host_list.append(str(ip_address(range_ip_start) + i))

    else:
        print('Неверный диапазон для проверки')
    return host_ping(sample_host_list, only_sum)


if __name__ == "__main__":
    host_range_ping()

"""

2. Задание на закрепление знаний по модулю json. Есть файл orders
в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий
его заполнение данными.

Для этого:
Создать функцию write_order_to_json(), в которую передается
5 параметров — товар (item), количество (quantity), цена (price),
покупатель (buyer), дата (date). Функция должна предусматривать запись
данных в виде словаря в файл orders.json. При записи данных указать
величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра.

"""

import json


def write_order_to_json(item, quantity, price, buyer, date):

    with open('orders.json', 'r', encoding='utf-8') as start_file:
        orders_data = json.load(start_file)

    with open('orders.json', 'w', encoding='utf-8') as filled_file:
        orders_list = orders_data['orders']
        order = {'item': item, 'quantity': quantity,
                 'price': price, 'buyer': buyer, 'date': date}
        orders_list.append(order)
        json.dump(orders_data, filled_file, indent=4)


write_order_to_json('monitor', '3', '35000', 'Fedorov S.P.', '03.04.2023')
write_order_to_json('keyboard', '5', '2500', 'Dmitriev A.R.', '02.04.2023')
write_order_to_json('mouse', '25', '1200', 'Nikolaev N.N.', '01.04.2023')

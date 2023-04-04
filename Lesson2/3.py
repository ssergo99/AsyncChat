"""

3. Задание на закрепление знаний по модулю yaml.
 Написать скрипт, автоматизирующий сохранение данных
 в файле YAML-формата.
Для этого:

Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа —
это целое число с юникод-символом, отсутствующим в кодировке
ASCII(например, €);

Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью
параметра default_flow_style, а также установить возможность работы
с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.

"""

import yaml

data_dict = {'products': ['iPhone 14', 'iPhone SE', 'iPhone 14 Pro Max'],
             'products_qty': 3,
             'products_price': {'iPhone 14': '900€',
                                'iPhone SE': '600€',
                                'iPhone 14 Pro Max': '1300€'}
             }

with open('file.yaml', 'w', encoding='utf-8') as start_file:
    yaml.dump(data_dict, start_file, default_flow_style=False, allow_unicode=True)

with open("file.yaml", 'r', encoding='utf-8') as end_file:
    dict_open = yaml.load(end_file, Loader=yaml.SafeLoader)

if data_dict == dict_open:
    print(f'Данные совпадают: {data_dict} = {dict_open}')
else:
    print(f'Что-то пошло не так: {data_dict} != {dict_open}')

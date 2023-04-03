"""

2. Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов
не используя методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.

"""


def print_info(word_list):
    for word_el in word_list:
        print(f'Тип переменной: {type(word_el)}')
        print(f'Содержимое переменной: {word_el}')
        print(f'Длина переменной: {len(word_el)}')
    print('____________________________')


bstr_class = b'class'
bstr_function = b'function'
bstr_method = b'method'

b_list = [bstr_class, bstr_function, bstr_method]

print_info(b_list)

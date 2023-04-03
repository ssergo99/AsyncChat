"""

4. Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

"""


def encode_to_bytes(word_list):
    word_list_bytes = []
    for word_el in word_list:
        word_b = word_el.encode('utf-8')
        word_list_bytes.append(word_b)
    print(word_list_bytes)
    print('_________________________')
    return word_list_bytes


def decode_to_str(b_word_list):
    word_list_str = []
    for word_el in b_word_list:
        b_el_str = word_el.decode('utf-8')
        word_list_str.append(b_el_str)
    print(word_list_str)
    print('_________________________')
    return word_list_str


word_1 = 'разработка'
word_2 = 'администрирование'
word_3 = 'protocol'
word_4 = 'standard'
word_list1 = [word_1, word_2, word_3, word_4]

b_word_list1 = encode_to_bytes(word_list1)
str_word_list = decode_to_str(b_word_list1)
if word_list1 == str_word_list:
    print('Верные преобразования')
else:
    print('Ошибка преобразований')

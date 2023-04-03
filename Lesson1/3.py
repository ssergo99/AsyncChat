"""

3. Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе с помощью маркировки b''.

"""


def check_words(word_list):
    for word_el in word_list:
        try:
            print(f'"{word_el}" - можно записать в байтовом типе: {bytes(word_el, "ascii")}')
        except UnicodeEncodeError:
            print(f'"{word_el}" - нельзя записать в байтовом типе')


word_1 = 'attribute'
word_2 = 'класс'
word_3 = 'функция'
word_4 = 'type'
word_list1 = [word_1, word_2, word_3, word_4]

check_words(word_list1)

"""

6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.

"""

from chardet.universaldetector import UniversalDetector

word_list = ['сетевое программирование', 'сокет', 'декоратор']
with open('test_file.txt', 'w') as file_to_write:
    for line in word_list:
        file_to_write.write(f'{line}\n')
file_to_write.close()

detector = UniversalDetector()
with open('test_file.txt', 'rb') as file_to_detect:
    for line in file_to_detect:
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    print(detector.result['encoding'])
file_to_detect.close()

with open('test_file.txt', encoding='utf-8') as file:
    for line in file.read():
        print(line)
file.close()

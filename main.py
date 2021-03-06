from distributed import Client
import re

def mapper(file):
    word_map = []
    for line in file:
        line = line.lower()
        words = [word for word in re.split("[^a-z']+", line) if word]
        for word in words:
            word_map.append(f'({word},1)')
    return word_map

def sorter(seq):
    seq.sort()
    return seq

def reducer(mapped_words):
    last_word = None
    word_count = 0
    counted_words = []
    for line in mapped_words:
        line = line[1:-1]
        word, count = line.split(',')
        count = int(count)

        if word == last_word:
            word_count += count
        else:
            if last_word:
                counted_words.append(f'{last_word} - {word_count}')
            last_word = word
            word_count = count

    counted_words.append(f'{last_word} - {word_count}')
    return counted_words

def main():
    file_content = open('177.txt', encoding='ISO-8859-1').readlines()
    # result = mapper(file_content)
    # result = sorter(result)
    # result = reducer(result)

    client = Client('tcp://192.168.1.40:8786')

    dsk = {
        'content': file_content,
        'mapper': (mapper, 'content'),
        'sorter': (sorter, 'mapper'),
        'reducer': (reducer, 'sorter')
    }

    result = client.get(dsk, 'reducer')
    for line in result:
        print(line)


if __name__ == '__main__':
    main()

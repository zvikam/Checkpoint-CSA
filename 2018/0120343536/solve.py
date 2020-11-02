import string
import sys


def display(m, s):
    return [m[c] if c in m else '?' for c in s]


map = {'_': '_'}
flag_data = 'KNBGB$_DV_$@Z$KWK@KB_AVG_GBTY_BDPG#FKWVD'
flag = 'flag{%s}'

flag_words = flag_data.split('_')
#flag_ords = [[ord(c) for c in w] for w in flag_words]
#flag_hords = [['%x' % ord(c) for c in w] for w in flag_words]

with open('dictionary.txt') as f:
    dictionary = [w.strip() for w in f.readlines()]

word_lengths = [len(w) for w in flag_words]

dict_words = [[w for w in dictionary if len(w) == l] for l in word_lengths]
#dict_ords = [[[ord(c) for c in w] for w in l] for l in dict_words]
#dict_hords = [[['%x' % ord(c) for c in w] for w in l] for l in dict_words]

sorted_lengths = sorted(range(len(word_lengths)), key=lambda k: word_lengths[k])

map = {'A': 'F', '@': 'U', '#': 'Y', 'B': 'E', 'D': 'N', 'G': 'R', 'F': 'P', 'K': 'T', 'N': 'H', 'P': 'C', 'T': 'A', 'W': 'I', 'V': 'O', 'Y': 'L', 'Z': 'B', '_': '_', '$': 'S'}

print(flag % ''.join(display(map, flag_data)))


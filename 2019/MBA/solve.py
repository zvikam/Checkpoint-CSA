import sys
import string
import glob
import base64
import itertools


def dict_product(dicts):
    """
    >>> list(dict_product(dict(number=[1,2], character='ab')))
    [{'character': 'a', 'number': 1},
     {'character': 'a', 'number': 2},
     {'character': 'b', 'number': 1},
     {'character': 'b', 'number': 2}]
    """
    return (dict(zip(dicts, x)) for x in itertools.product(*dicts.values()))

quote = "One must divide one's time between politics and equations. But our equations are much more important to me, because politics is for the present, while our equations are for eternity."

#clear = ''.join([c for c in quote if c not in string.punctuation])
words = quote.split()

message_files = glob.glob("./fs/message_*")

messages = {}
order = []
for m in message_files:
    uuid = m.split('_')[1]
    with open(m, 'r') as fin:
        data = fin.read()
    word = base64.b64decode(data)
    messages[uuid] = word.decode('utf-8')
    order.append(uuid)

items = [None] * len(words)
locations = {}
for m in messages:
    found = [i for i, x in enumerate(words) if x == messages[m]]
    locations[m] = found
    for f in found:
        items[f] = m

for m in messages:
    print(m, messages[m], locations[m])

bin_files = glob.glob("./fs/bin_*")
binaries = {}
for b in bin_files:
    uuid = b.split('_')[1]
    with open(b, 'rb') as fin:
        data = fin.read()
    binaries[uuid] = data

#for o in dict_product(locations):
composed = b''
for i in items:
    print("appending", len(binaries[i]), i)
    composed += binaries[i]

with open('composed.bin', 'wb') as fout:
    fout.write(composed)

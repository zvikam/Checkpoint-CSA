import itertools
import sys


def xor_crypt_string(data, key='xor', encode=False, decode=False):
    from itertools import izip, cycle
    import base64
    if decode:
        data = base64.decodestring(data)
    xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(data, cycle(key)))
    if encode:
        return base64.encodestring(xored).strip()
    return xored

with open(sys.argv[1], 'rb') as fin:
    print(xor_crypt_string(fin.read()))

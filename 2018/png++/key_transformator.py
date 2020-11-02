import sys


def transform(key):
    new_key = ''.join([chr((ord(c)+1) % 256) for c in key])
    return new_key

import key_transformator
import random
import string

key_length = 4

KEY = [65, 90, 79, 68]

# AZOD
def generate_initial_key():
    return ''.join(chr(c) for c in KEY)


def xor(s1, s2):
    res = [chr(0)]*key_length
    for i in range(len(res)):
        q = ord(s1[i])
        d = ord(s2[i])
        k = q ^ d
        res[i] = chr(k)
    res = ''.join(res)
    return res


with open('encrypted.png', 'rb') as f:
    img = f.read()

key = generate_initial_key()

dec_data = ''
for i in range(0, len(img), key_length):
    dec = xor(img[i:i+key_length], key)
    key = key_transformator.transform(key)
    dec_data += dec

with open('flag.png', 'wb') as f:
    f.write(dec_data)

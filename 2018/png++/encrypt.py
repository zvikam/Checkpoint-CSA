import key_transformator
import random
import string

# header:       137, 80, 78, 71, 13, 10, 26, 10
# encrypted:    200, 10, 1, 3, 79, 81, 74, 79
# key:          65, 90, 79, 68,  66, 91, 80, 69
key_length = 4


def generate_initial_key():
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(4))


def xor(s1, s2):
    res = [chr(0)]*key_length
    for i in range(len(res)):
        q = ord(s1[i])
        d = ord(s2[i])
        k = q ^ d
        res[i] = chr(k)
    res = ''.join(res)
    return res


def add_padding(img):
    l = key_length - len(img)%key_length
    img += chr(l)*l
    return img


with open('flag.png', 'rb') as f:
    img = f.read()

img = add_padding(img)
key = generate_initial_key()

enc_data = ''
for i in range(0, len(img), key_length):
    enc = xor(img[i:i+key_length], key)
    key = key_transformator.transform(key)
    enc_data += enc

with open('encrypted.png', 'wb') as f:
    f.write(enc_data)
import base64


with open('ciphertext') as fin:
    ciphertext=fin.read()

ciphertext_1=base64.b64decode(ciphertext)

ciphertext_2=''.join([chr(255-i) for i in ciphertext_1])

print(ciphertext_2)

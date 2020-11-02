import sys
import time
from socket import create_connection


SERVER = ('35.157.111.68', 20098)
RECV_SIZE = 256


def decode(s, k):
    a = s.split('0x')
    a = a[1:]
    b = [int(x,16) ^ k for x in a]
    c = ['%x' % x for x in b]
    d = []
    for x in c:
        d.append(x[:2])
        d.append(x[2:])
    r = [chr(int(x,16)) for x in d]
    return ''.join(r)


def main():
    sample = '0x6bf50x59f30x1ce40x53e80x1cfb0x5df10x50b10x1cd40x1cea0x55f10x50bd0x5ef80x1ce90x54f80x4ef80x1ce90x53bd0x5ffc0x48fe0x54bd0x45f20x49bd0x11bd0x6bf40x48f50x1cf10x53eb0x59b10x1ce90x54f80x1cfb0x50f20x53ef'
    key = 0x3c9d
    print(decode(sample, key))

    file = '/usr/pRivat3.txt'

    conn = create_connection(SERVER)
    state = 1
    while True:
        response = conn.recv(RECV_SIZE).splitlines()
        for line in response:
            print(line)
            if state == 1:
                conn.send('1 5 HELLO\n')
                state = 2
            elif state == 2:
                conn.send('2 3 XOR\n')
                state = 3
            elif state == 3:
                key = int(line.split()[2], 16)
                conn.send('3 %d %s\n' % (len(file), file))
                state = 4
            elif state == 4:
                data = line.split()[2]
                print(decode(data, key))
                return

if __name__ == '__main__':
    main()
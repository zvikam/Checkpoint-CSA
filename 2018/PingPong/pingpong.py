import sys
import time
from socket import create_connection


SERVER = ('35.157.111.68', 10199)
RECV_SIZE = 256


def main():
    conn = create_connection(SERVER)
    while True:
        response = conn.recv(RECV_SIZE).splitlines()
        for line in response:
            print(line)
            if 'Welcome!' in line:
                continue
            if 'flag' in line:
                return
            num = line.split()[-1]
            conn.send('%s\n' % num)

if __name__ == '__main__':
    main()

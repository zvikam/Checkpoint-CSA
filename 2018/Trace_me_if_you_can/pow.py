import hashlib
import itertools
import re
import string
import sys
from socket import create_connection


valids = string.ascii_letters + string.digits
SERVER = ('35.194.63.219', 2002)


def find_sha256(suffix, hash):
    hash = hash.decode('hex')
    options = itertools.product(valids, repeat=4)
    for o in options:
        m = hashlib.sha256()
        s = ''.join(o) + suffix
        m.update(s)
        h = m.digest()
        if h == hash:
            return ''.join(o)
    return None


def main():
    if len(sys.argv) == 1:
        answer = '2 1 50 3 2 1 7 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 100 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3\n'
        print('[+] talking to server')
        conn = create_connection(SERVER)
        n = 0
        while n < 3:
            response = conn.recv(1024).splitlines()
            for line in response:
                print(line)
                n += 1
                if 'sha256(ABCD' in line:
                    parts = re.split('\+|\)| ', line)
                    hash = find_sha256(parts[1], parts[4])
        print('[+] found %s' % hash)
        conn.send(hash)
        print(conn.recv(512))
        print('[+] sending response "%s"' % answer)
        conn.send(answer)
        print(conn.recv(512))
    else:
        print('[+] searching for hash')
        print(find_sha256(sys.argv[1], sys.argv[2]))


if __name__ == '__main__':
    main()

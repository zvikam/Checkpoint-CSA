from __future__ import print_function
import sys


def str2ushort(a):
    l = ord(a[0])
    h = ord(a[1])
    return 256*ord(a[1]) + ord(a[0])


def decode(f):
    # GOAL: reconstruct 'ks' from the file
    f.seek(0)
    ks = []
    mp = ''

    start = 0
    data = f.read()
    begin = data.find('RDBNB', start)
    if begin < 0:
        return
    end = data.find('\x00', begin)
    if end < 0:
        return
    comment = data[begin+5:end]
    while True:
        i = data.find('\x21\xF9\x04\x05', start)
        if i < 0:
            break
        pos = i + 4
        delay = str2ushort(data[pos:pos+2])
        pos += 2
        tidx = ord(data[pos])
        pos += 1
        tmp = ord(data[pos])
        assert data[pos] == '\x00'
        pos += 1
        tmp = ord(data[pos])
        assert data[pos] == '\x2c'
        pos += 1
        x = str2ushort(data[pos:pos+2])
        pos += 2
        y = str2ushort(data[pos:pos+2])
        pos += 2
        w = str2ushort(data[pos:pos+2])
        pos += 2
        h = str2ushort(data[pos:pos+2])
        pos += 2
        tmp = ord(data[pos])
        assert data[pos] == '\x00'
        pos += 1

        if x == 0:
            if y == 0:
                mpindx = w * h
            elif y == 1:
                mpindx = h >> 2
            else:
                raise Exception("illegal y=%d for x=0" % y)
        elif x == 1:
            mpindx = y >> 1
        else:
            raise Exception("illegal x=%d" % x)

        isup = tidx & 0x01

        ks.append((mpindx, isup))

        start = pos

    print(len(comment), comment)
    print(ks)

    flag = []
    for x in ks:
        c = comment[x[0]]
        flag.append(c if x[1] == 1 else c.lower())

    print(''.join(flag))

    return 0


if __name__ == '__main__':
    assert len(sys.argv) == 2, 'bad input'
    fpath = sys.argv[1]

    f = open(fpath, 'rb')
    rv = decode(f)
    sys.exit(rv)

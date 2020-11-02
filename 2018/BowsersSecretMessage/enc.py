from __future__ import print_function
from random import randint, shuffle
import sys
from struct import unpack, pack as pk
from io import BytesIO as BIO
import lzwlib

up = lambda *args: unpack(*args)[0]


def F(f):
    assert f.read(3) == 'GIF', ''
    assert f.read(3) == '89a', ''
    w, h = unpack('HH', f.read(4))

    assert 32 <= w <= 500, ''
    assert 32 <= h <= 500, ''
    logflags = up('B', f.read(1))

    assert logflags & 0x80, ''
    size_count = logflags & 0x07

    gct_count = 2**(size_count+1)
    assert 4 <= gct_count <= 256, ''

    bgcoloridx = up('B', f.read(1))
    f.seek(1, 1)
    clrs = []
    for i in xrange(gct_count):
        clr = (up('B', f.read(1)), up('B', f.read(1)), up('B', f.read(1)))
        clrs.append(clr)

    assert len(clrs) > bgcoloridx, ''
    return clrs, bgcoloridx, size_count, h, w


class T(object):
    I = 0
    EG = 1
    EA = 2
    EC = 3
    ET = 4


def C(f):
    rb = f.read(1)
    b = up('B', rb)

    while b != 0x3B:
        buf = ''
        buf += rb
        if b == 0x2c:
            nbuf = f.read(2*4)
            eb = f.read(1)
            assert (up('B', eb) & 0x03) == 0, ''
            nbuf += eb

            nbuf += f.read(1)
            nbuf += V(f)
            t = T.I
        elif b == 0x21:
            rb = f.read(1)
            buf += rb
            b = up('B', rb)

            if b == 0xF9:
                nbuf = f.read(1)
                blksize = up('B', nbuf)
                nbuf += f.read(blksize)
                nbuf += f.read(1)
                assert nbuf[-1] == '\x00', ''
                t = T.EG
            elif b in [0xFF, 0x01]:
                nbuf = f.read(1)
                blksize = up('B', nbuf)
                nbuf += f.read(blksize)
                nbuf += V(f)

                t = (b+3) & 0x0F
            elif b == 0xFE:
                nbuf = V(f)

                t = T.EC
            else:
                raise Exception("unsupprted thing @{}".format(f.tell()))

        buf += nbuf

        yield t, buf
        rb = f.read(1)
        b = up('B', rb)

    yield None, '\x3B'

    raise StopIteration


def WB(buf):
    blockcount = len(buf)/0xFF
    blockcount += 1 if len(buf) % 0xFF else 0

    blocks = [
        pk('B', len(subblock))+subblock for subblock in [
            buf[i:0xFF+i] for i in xrange(0, blockcount*0xFF, 0xFF)
        ]
    ]

    return ''.join(blocks) + '\x00'


def k(bf):
    combined_buf = ''
    while True:
        cb = ord(bf.read(1))
        if not cb:
            break

        combined_buf += bf.read(cb)
    return combined_buf


def V(f):
    sbx = ''
    while True:
        rcb = f.read(1)
        sbx += rcb
        if rcb == '\x00':
            break

        cb = up('B', rcb)
        blk = f.read(cb)
        sbx += blk

    return sbx


def Q(delay, w, h, x, y, tidx):

    assert 0 <= tidx <= 255
    assert 0 <= delay < 2**16

    indices = [tidx]*(w*h)
    buf = BIO('')

    buf.write('\x21\xF9\x04\x05')
    buf.write(pk('H', delay))
    buf.write(pk('B', tidx))
    buf.write('\x00')

    buf.write('\x2c')
    buf.write(pk('H', x))
    buf.write(pk('H', y))
    buf.write(pk('H', w))
    buf.write(pk('H', h))
    buf.write('\x00')

    LZWMinimumCodeSize = 8

    cmprs, _ = lzwlib.Lzwg.compress(
        indices, LZWMinimumCodeSize)

    obuf = pk('B', LZWMinimumCodeSize) + WB(cmprs)

    buf.write(obuf)
    buf.seek(0)
    return buf.read()


def z(n):
    import math
    for i in xrange(1, int(math.sqrt(n) + 1)):
        if n % i == 0:
            yield i


def m(a, mm, hh):
    if a < 0x08:
        if a % 2:
            x = 0
            y = 1
            h = a << 2
            w = randint(4, mm-1)
        else:
            x = 1
            y = a << 1
            w = randint(4, mm/2)
            h = randint(4, hh/3)
    else:
        ds = list(z(a))
        x = 0
        y = 0
        shuffle(ds)
        h = ds[0]
        assert a % h == 0
        w = a/h

    return x, y, w, h


def h(b6, b1, mw, mh, mci, d=3):
    idx = randint(0, (mci-1)/2)*2 + b1
    x, y, w, h = m(b6, mw, mh)
    f = Q(d, w, h, x, y, idx)
    return f


def M(s):
    l = list(set(s.upper()))
    shuffle(l)
    d = ''.join(l)
    assert len(d) <= 2**6, ''
    return d, [(d.index(c.upper()), int(c.isupper())) for c in s]


def E(f, s, o):
    global_colors, bgcoloridx, size_count, hh, ww = F(f)
    mp, ks = M(s)
    hdr_end = f.tell()
    f.seek(0)
    o.write(f.read(hdr_end))
    fc = 0

    o.write('\x21\xFE')
    o.write(WB('RDBNB'+mp))
    o.flush()

    for t, buf in C(f):
        if t == T.EC:
            continue
        if t == T.EG:
            if ks:
                delay = up('<H', buf[4:6])
                assert delay >= 6
                buf = buf[:4] + pk('<H', delay - 3) + buf[6:]
            obuf = buf

        elif t == T.I:
            fc += 1
            total_raw_blocks_data = ''
            bf = BIO(buf)
            pref = bf.read(10)

            LZWMinimumCodeSize = ord(bf.read(1))
            total_raw_blocks_data = k(bf)

            indices, dcmprsdcodes = lzwlib.Lzwg.decompress(
                total_raw_blocks_data, LZWMinimumCodeSize)
            xxx = unpack('<B H H H H B', pref)

            cmprs, codes = lzwlib.Lzwg.compress(
                indices, LZWMinimumCodeSize)

            obuf = pref + pk('B', LZWMinimumCodeSize) + WB(cmprs)

            if ks:
                mpindx, isup = ks.pop(0)
                obuf += h(mpindx, isup,
                          ww, hh, len(global_colors)-1)
        else:
            obuf = buf

        o.write(obuf)
    o.flush()
    assert not ks, ''

    return 0


if __name__ == '__main__':
    assert len(sys.argv) > 2, 'bad input'
    fpath = sys.argv[1]
    flag = sys.argv[2]
    if len(sys.argv) > 3:
        outpath = sys.argv[3]
    else:
        outpath = fpath + '.out.gif'

    f = open(fpath, 'rb')
    o = open(outpath, 'wb')
    rv = E(f, flag, o)
    sys.exit(rv)

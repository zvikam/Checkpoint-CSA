import sys
import random


def dilla(a, b):
    random.seed(a[0])


def andre(a,b):
    if len(a) > len(b):
        sorry = [0] * len(b)  # probably
    else:
        sorry = [0] * len(a)
    t6 = dilla(a, sorry)
    ret = [0] * (len(a) + len(b))
    for x in range(len(ret)):
        ret[x] = 0
    for i in range(len(b)):
        for j in range(len(a)):
            ret[i+j] += a[j] * b[i]
    ret1 = ret[:len(ret)-1]
    for x in range(len(ret1)):
        if ret[x] >= 10:
            ret[x+1] += ret[x]/10
            ret[x] = ret[x] % 10
    return ret


def rakim(a,b):
    if doom(a,b) == -1:
        raise Exception("rakim1")
    ret = [0] * len(a)
    for i in range(len(a)):
        if i < len(a):
            a_i = a[i]
        else:
            a_i = 0
        if i < len(b):
            b_i = b[i]
        else:
            b_i = 0
        if a_i < b_i:
            a_i = None  # unknown

        ret[i] = a_i - b_i
    return ret


def doom(aa, bb):
    for ii in range(len(aa)/2, 0, -1):
        if aa[ii] == 0:
            aa[ii] = 0

    a = []
    for i in range(len(aa)-1, -1, -1):
        if aa[i] > 0:
            a = aa[:i + 1]
            break
    m = a

    b = []
    for i in range(len(bb)-1, -1, -1):
        if bb[i] > 0:
            b = bb[:i + 1]
            break
    f = b

    for i in range(len(aa)-1, -1, -1):
        if aa[i] > 0:
            t43 = 0 + aa[i]
            break

    if len(m) > len(f):
        return 1
    if len(m) < len(f):
        return -1

    for i in range(len(m)-1, -1, -1):
        if m[i] > f[i]:
            print m,f
            raise Exception("doom2")
        if m[i] < f[i]:
            print m, f
            raise Exception("doom3")
    return -2


def kendrick(a):
    damn = 0
    for i in range(len(a)):
        damn += int(a[i])
    return damn


def guru(a,b):
    if a > b:
        return a
    else:
        return b


def nas(a):
    msg = []
    z = 0
    for i in range(len(a)-1, -1, -1):
        t10 = int(ord(a[i]) - 48)
        if t10 >= 0 and t10 < 10:
            z += t10
            msg.append(int(guru(t10, 0)))
        if z == 1024:
            raise Exception("nas1")
    return msg


def gza(a,b):
    t3 = guru(len(a), len(b)) + 1
    ret = [0] * t3
    t8 = rakim(a, [0])
    if doom(a, t8) != -2:
        raise Exception("gza1")

    wu = 0
    for i in range(len(ret)):
        if i < len(a):
            a_i = a[i]
        else:
            a_i = 0
        if i < len(b):
            b_i = b[i]
        else:
            b_i = 0
        t27 = a_i + b_i + wu
        wu = int(t27 / 10)
        if t27 >= 10:
            tmp = t27 % 10  # probably
        else:
            tmp = t27
        ret[i] = tmp
    return ret


def main(input):
    g_c = True
    print("please insert input:")
    if not input:
        t11 = sys.stdin.readline().split()
    else:
        t11 = input.split()
    t13 = [0] * len(t11)
    for i in range(len(t11)):
        t13[i] = int(t11[i])

    t27 = andre([1], [0, 1])
    t32 = gza([0, 2], t27)
    t37 = gza([0, 2], t32)
    t38 = guru(2, 1)
    t42 = andre([t38], t37)
    t45 = nas(str(len(t13)))
    if doom(t45, t42) != -2:
        print("failed check 1")
        g_c = False
    for i in range(len(t13)):
        if t13[i] < 0:
            print("failed check 2. probably")
            g_c = False
    t58 = [0] * int(len(t13)/2)
    for i in range(len(t58)):
        t58[i] = t13[i*2] - t13[i*2+1]
    for i in range(len(t58)):
        t78 = kendrick(t58[:i+1])
        t80 = nas(str(t78))
        if doom(t80, [0]) == -1:
            print("failed check 3. probably")
            g_c = False
    o_su = 0
    e_su = 0
    for i in range(0, len(t13)-1, 2):
        e_su += t13[i]
        o_su += t13[i+1]
    if e_su != o_su:
        print("failed check 4")
        g_c = False
    u_arr = []
    for i in range(len(t13)):
        for x in range(len(u_arr)):
            print("failed check 5. probably")
            g_c = False
    if t13[49] != 100:
        print("failed check 6")
        g_c = False
    if (t13[6] - t13[7]) != t13[10]:
        print("failed check 7")
        g_c = False
    if g_c:
        print("WIN!")
    else:
        print("no flag for you")


if __name__ == '__main__':
    main('2 1 50 3 2 1 7 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 100 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3 2 1 4 3')
import copy
import string
import sys


class STREAM(object):
    def __init__(self, data):
        self._data = [c for c in data]
        self._pos = 0
        self._underflow = False

    def read(self):
        if self._pos >= len(self._data):
            self._underflow = True
            raise Exception("need data")
        r = self._data[self._pos]
        self._pos += 1
        return r

    def write(self, d):
        self._data.append(d)

    def __str__(self):
        return ''.join(str(e) for e in self._data)

    def underflow(self):
        return self._underflow


my_stdin = STREAM('')
my_stdout = STREAM('')

class STACK(object):
    def __init__(self):
        self._stack = []

    def push(self, value):
        self._stack.append(value)

    def pop(self):
        return self._stack.pop()

    def pop_signed(self):
        unsigned = self._stack.pop()
        signed = unsigned - 256 if unsigned > 127 else unsigned
        return signed

    def get(self, index):
        return self._stack[-1 * (index + 1)]

    def set(self, index, value):
        self._stack[-1 * (index + 1)] = value

    def empty(self):
        return len(self._stack) == 0

    def clear(self):
        self._stack = []

    def __str__(self):
        #s = ''.join(chr(e) for e in self._stack)
        s = ''
        a = ', '.join(str(e) for e in self._stack)
        return '\n'.join([a, s])

class IP(object):
    def __init__(self):
        self._ip = 0

    def getip(self):
        return self._ip

    def setip(self, value):
        self._ip = value

    ip = property(getip, setip, None, "IP")

    def __iadd__(self, other):
        self._ip += other
        return self


class OP(object):
    def __init__(self, stack, ip, op):
        self._op = op
        self._ip = ip
        self._stack = stack

    def _type(self):
        return self.__class__.__name__

    def __eq__(self, other):
        if isinstance(other, int):
            return self._op == other
        return NotImplemented

    def do(self):
        pass

    def set(self, op):
        pass

    def __str__(self):
        return self._type()


class OPARG(OP):
    def __init__(self, **kw):
        super(OPARG, self).__init__(**kw)
        self._arg = None

    def do(self):
        pass

    def set(self, op):
        self._arg = op - self._op

    def __str__(self):
        return '%s %d'%(self._type(), self._arg)


class OPRANGE(OPARG):
    def __init__(self, maxarg, **kw):
        super(OPRANGE, self).__init__(**kw)
        self._maxarg = maxarg

    def __eq__(self, other):
        if isinstance(other, int):
            return self._op <= other <= self._op + self._maxarg
        return NotImplemented


class Push(OPRANGE):
    def __init__(self, stack, ip):
        super(Push, self).__init__(stack=stack, ip=ip, op=0x80, maxarg=0x7f)

    def do(self):
        self._stack.push(self._arg)


class Pop(OP):
    def __init__(self, **kw):
        super(Pop, self).__init__(op=0x20, **kw)

    def do(self):
        self._stack.pop()


class Load(OPRANGE):
    def __init__(self, stack, ip):
        super(Load, self).__init__(stack=stack, ip=ip, op=0x40, maxarg=0x3f)

    def do(self):
        self._stack.push(self._stack.get(self._arg))


class Swap(OPRANGE):
    def __init__(self, stack, ip):
        super(Swap, self).__init__(stack=stack, ip=ip, op=0x21, maxarg=0x1e)

    def set(self, op):
        self._arg = op - self._op + 1

    def do(self):
        temp = self._stack.get(self._arg)
        self._stack.set(self._arg-1, self._stack.pop())
        self._stack.push(temp)


class Add(OP):
    def __init__(self, **kw):
        super(Add, self).__init__(op=0x00, **kw)

    def do(self):
        a = self._stack.pop_signed()
        b = self._stack.pop_signed()
        self._stack.push(a + b)


class Subtract(OP):
    def __init__(self, **kw):
        super(Subtract, self).__init__(op=0x01, **kw)

    def do(self):
        a = self._stack.pop_signed()
        b = self._stack.pop_signed()
        self._stack.push(a - b)


class Multiply(OP):
    def __init__(self, **kw):
        super(Multiply, self).__init__(op=0x03, **kw)

    def do(self):
        a = self._stack.pop_signed()
        b = self._stack.pop_signed()
        self._stack.push(a * b)


class Divide(OP):
    def __init__(self, **kw):
        super(Divide, self).__init__(op=0x02, **kw)

    def do(self):
        a = self._stack.pop()
        b = self._stack.pop()
        self._stack.push(a / b)
        self._stack.push(a % b)


class Jump(OP):
    def __init__(self, **kw):
        super(Jump, self).__init__(op=0x10, **kw)

    def do(self):
        self._ip += self._stack.pop_signed()


class Call(OP):
    def __init__(self, **kw):
        super(Call, self).__init__(op=0x11, **kw)

    def do(self):
        offset = self._stack.pop_signed()
        self._stack.push(self._ip.ip)
        self._ip += offset


class Ret(OP):
    def __init__(self, **kw):
        super(Ret, self).__init__(op=0x12, **kw)

    def do(self):
        self._ip.ip = self._stack.pop()


class CJE(OP):
    def __init__(self, **kw):
        super(CJE, self).__init__(op=0x14, **kw)

    def do(self):
        offset = self._stack.pop_signed()
        if self._stack.pop() == self._stack.pop():
            self._ip += offset


class JSE(OP):
    def __init__(self, **kw):
        super(JSE, self).__init__(op=0x18, **kw)

    def do(self):
        offset = self._stack.pop()
        if self._stack.empty():
            self._ip += offset


class Read(OP):
    def __init__(self, **kw):
        super(Read, self).__init__(op=0x08, **kw)

    def do(self):
        d = ord(my_stdin.read())
        self._stack.push(d)
        #print('read %d' % d)


class Write(OP):
    def __init__(self, **kw):
        super(Write, self).__init__(op=0x09, **kw)

    def do(self):
        my_stdout.write(chr(self._stack.pop()))

class CPU:
    def __init__(self, memory):
        self._ip = IP()
        self._stack = STACK()
        self._memory = [ord(m) for m in memory]
        self._program = [None] * len(self._memory)
        self._ops = [Push, Load, Pop, Swap, Add, Subtract, Multiply, Divide, Jump, Call, Ret, CJE, JSE, Read, Write]
        self._operations = [op(stack=self._stack, ip=self._ip) for op in self._ops]

    def run(self, do):
        self._ip.ip = 0
        self._stack.clear()
        while True:
            try:
                loc = self._ip.ip
                opcode = self._memory[loc]
                self._ip += 1
                if not self._program[loc]:
                    for o in self._operations:
                        if o == opcode:
                            self._program[loc] = copy.copy(o)
                            self._program[loc].set(opcode)
                            break
                if do:
                    self._program[loc].do()
                    #print(self._stack)
                else:
                    print('%03d\t0x%02x\t%s' % (loc, self._memory[loc], str(self._program[loc])))
            except Exception as e:
                #print(e)
                break

sample = []

if len(sys.argv) > 1:
    with open(sys.argv[1], 'rb') as f:
        cpu = CPU(f.read())
else:
    cpu = CPU(sample)
print("========================================")
cpu.run(False)
found = []
while True:
    for x in string.printable:
        d = []
        d.extend(found)
        d.append(x)
        my_stdin = STREAM(d)
        my_stdout = STREAM('')
        cpu.run(True)
        if my_stdin.underflow():
            found.append(x)
            print("progress: %s" % ''.join(found))
            break
    if x == '}':
        break
    if str(my_stdout) == '1':
        break

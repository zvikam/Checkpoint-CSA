import sys

class CPU:
    def __init__(self, memory):
        self._ip = 0
        self._stack = []
        self._memory = [ord(m) for m in memory]
        self._operations = {0x09: self.write,
                      0x08: self.read,
                      0x18: self.jse,
                      0x14: self.cje,
                      0x12: self.ret,
                      0x11: self.call,
                      0x10: self.jump,
                      0x02: self.divide,
                      0x03: self.mul,
                      0x01: self.subtract,
                      0x00: self.add,
                      0x20: self.pop }

    def push(self, value):
        self._stack.append(value)

    def pop(self):
        return self._stack.pop()

    def load(self, index):
        self.push(self._stack[-1 * index])

    def swap(self, index):
        temp = self._stack[-1 * index]
        self._stack[-1 * index] = self.pop()
        self.push(temp)

    def add(self):
        self.push(self.pop() + self.pop())

    def subtract(self):
        self.push(self.pop() - self.pop())

    def mul(self):
        self.push(self.pop() * self.pop())

    def divide(self):
        a = self.pop()
        b = self.pop()
        self.push(a / b)
        self.push(a % b)

    def jump(self):
        self._ip += self.pop()

    def call(self):
        offset = self.pop()
        self.push(self._ip)
        self._ip += offset

    def ret(self):
        self._ip = self.pop()

    def cje(self):
        offset = self.pop()
        if self.pop() == self.pop():
            self._ip += offset

    def jse(self):
        offset = self.pop()
        if len(self._stack) == 0:
            self._ip += offset

    def read(self):
        input = sys.stdin.read(1)
        self.push(ord(input[0]))

    def write(self):
        sys.stdout.write(self.pop())

    def execute(self, opcode):
        if opcode in self._operations:
            self._operations[opcode]()
        elif opcode > 0x20 and opcode <= 0x3F:
            index = opcode - 0x20
            self.swap(index)
        elif opcode >= 0x40 and opcode <= 0x7F:
            offset = opcode - 0x40
            self.load(offset)
        elif opcode >= 0x80 and opcode <= 0xFF:
            value = opcode - 0x80
            self.push(value)

    def run(self):
        while True:
            opcode = self._memory[self._ip]
            self._ip += 1
            self.execute(opcode)


sample = []

if len(sys.argv) > 1:
    with open(sys.argv[1], 'rb') as f:
        cpu = CPU(f.read())
else:
    cpu = CPU(sample)
try:
    cpu.run()
except Exception as e:
    print(e)


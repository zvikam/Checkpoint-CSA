import copy
import hashlib
import re
import sys
from collections import Counter


class CodeBlock(object):
    def __init__(self, label, code=None):
        self.label = label
        self.code = code if code else []
        self._hash = None
        self.count = 1

    def add_line(self, s):
        self.code.append(s)

    def repeat(self):
        self.count += 1

    def get_hash(self):
        if not self._hash:
            m = hashlib.md5()
            for l in self.code:
                m.update(str(l))
            self._hash = m.digest()
        return self._hash

    def __eq__(self, other):
        return self._hash == other.get_hash()

    def __str__(self):
        if self.count > 1:
            s = ('%s: (x%d)' % (str(self.label), self.count))
        else:
            s = ('%s:' % str(self.label))
        for line in self.code:
            s += '\n\t'
            s += str(line)
        return s


class GoFunction(object):
    def __init__(self, name):
        self.name = name
        self.code = [CodeBlock('body')]
        self.block_signature = re.compile(r'^\.(\d+):')

    def add_line(self, s):
        m = self.block_signature.match(s)
        if m:
            l = m.groups()
            self.code.append(CodeBlock(l[0]))
        else:
            self.code[-1].add_line(s)

    def __str__(self):
        s = '======================================================'
        s += '\n[+] '
        s += self.name
        for block in self.code:
            s += '\n'
            s += str(block)
        return s

    @staticmethod
    def _longest_repetition(iterable):
        times = 2
        for n in range(1, len(iterable) / times + 1)[::-1]:
            substrings = [iterable[i:i + n] for i in range(len(iterable) - n + 1)]
            freqs = Counter(substrings)
            if freqs.most_common(1)[0][1] >= 3:
                seq = freqs.most_common(1)[0][0]
                break
        return seq,n

    def fold(self):
        new_code = copy.copy(self.code)
        changed = True
        while changed:
            changed = False
            for p in range(0, len(new_code)):
                for l in range(1, len(new_code) - p):
                    segments = [new_code[i:i + l] for i in xrange(p, len(new_code), l)]
                    new = [CodeBlock('folded', segments[0])]
                    for si in range(1, len(segments)):
                        new_block = CodeBlock('folded', segments[si])
                        if new[-1].get_hash() != new_block.get_hash():
                            new.append(new_block)
                        else:
                            new[-1].repeat()
                            changed = True
                    if changed:
                        new_code = new
                        break
                if changed:
                    break
            spread = []
            for b in new_code:
                if b.label != 'folded' or b.count > 1:
                    spread.append(b)
                else:
                    spread.extend(b.code)
            new_code = spread
        self.code = spread
        pass

class TraceLine(object):
    def __init__(self, level, func):
        self._func = func
        self._level = level

    def __str__(self):
        return ''.join(['  '] * self._level) + self._func.name


code_trace = []
code_functions = []
current_func = -1
stack = []
with open('b23456.txt') as fin:
    for line in fin.readlines():
        if line.startswith('Starting '):
            func = GoFunction(line.split()[1])
            current_func += 1
            code_trace.append(TraceLine(current_func, func))
            stack.append(func)
        elif line.startswith('Returning from '):
            #code_trace.append(''.join(['  '] * current_func) + line.strip())
            code_functions.append(stack.pop())
            current_func -= 1
        else:
            stack[current_func].add_line(line.strip())

num_functions = len(code_functions)
#function_names = set()
#unique_functions = [f for f in code_functions if f.name not in function_names and not function_names.add(f.name)]
unique_functions = sorted(code_functions, key=lambda x: x.name)
num_functions = len(unique_functions)

begin = False
for line in code_trace:
    txt = str(line)
    if 'main.main' in txt:
        begin = True
    if begin:
        print(txt)

index = 0
for f in unique_functions:
    if 'main.' in f.name and '.init' not in f.name:
        #f.fold()
        with open('ssa/%s.%i.ssa' % (f.name, index), "w") as file:
            file.write(str(f))
        index += 1

import string
import hashlib
from os import walk

root = './blocks'

class Node():
    def __init__(self, name, id=0):
        self._sonNodes = []
        self._id = id
        self._name = name
        self._hash = ''
        self._data = ''

    def calcHash(self, value):
        return hashlib.md5(value.encode('utf-8')).hexdigest()
        
    def hash(self):
        value = ''
        if len(self._sonNodes) > 0:
            for s in self._sonNodes:
                value += s.hash()
        self._hash = self.calcHash(value + self._data)
        return self._hash
    
    def append(self, s):
        self._sonNodes.append(s)
        
    def print(self, level=0):
        print(('\t' * level) + str(self._hash))
        if len(self._sonNodes) > 0:
            for s in self._sonNodes:
                s.print(level+1)


class TX(Node):
    def __init__(self, name):
        Node.__init__(self, name)
        self._id = int(name.split('_')[1])
        
    def read(self, dir):
        with open(root + '/' + dir + '/' + self._name) as fin:
            self._data = fin.read()


class Block(Node):
    def __init__(self, name):
        Node.__init__(self, name)
        self._iv = ''
        parts = name.split('-')
        self._id = int(parts[0].split('_')[1])
        self._height = int(parts[1].split('_')[1])
        self._sons = int(parts[2].split('_')[1])
        self._blockHash = ''
        self._txroot = ''
        self._txs = []
        
    def process(self, iv):
        self._iv = iv
        files = []
        for (dirpath, dirnames, filenames) in walk(root + '/' + self._name):
            files.extend(filenames)
            break
        print("found %d transactions" % len(files))
        for f in files:
            tx = TX(f)
            tx.read(self._name)
            self._txs.append(tx)
        self._txs.sort(key=lambda o: o._id)
        bottom = self._txs
        top = []
        for l in range(self._height-1):
            for b in bottom:
                if (b._id % self._sons) == 0:
                    n = Node(str(len(top)), len(top))
                    top.append(n)
                n.append(b)
            bottom = top
            top = []
        for b in bottom:
            self.append(b)
        self._txroot = self.hash()
        self._blockHash = self.calcHash(self._iv + self._txroot)
        self.print()

        
def main():
    dirs = []
    for (dirpath, dirnames, filenames) in walk(root):
        dirs.extend(dirnames)
        break

    blocks = []
    iv = "a861f335d4d457a7c1d00640da380dc4"
    for d in dirs:
        b = Block(d)
        blocks.append(b)
    blocks.sort(key=lambda o: o._id)
    
    for b in blocks:
        b.process(iv)
        print("Block(%d, %s) = %s" % (b._id, b._iv, b._blockHash))
        iv = b._blockHash

if __name__ == '__main__':
    main()

import os
import zipfile
import rarfile

subdir = 'archives'
files = [f for f in os.listdir(subdir) if os.path.isfile(os.path.join(subdir, f))]
l = [None] * len(files)
visited = [False] * len(files)

for f in sorted(files):
    file = os.path.join(subdir, f)
    try:
        ar = zipfile.ZipFile(file)
    except:
        ar = rarfile.RarFile(file)

    _, ext = os.path.splitext(file)

    comment = [m.rstrip() for m in ar.comment.split(',')]
    l[int(ext[1:])] = comment
      
visited = [False] * len(l)
i = 0
s = []
while not all(visited):
    s.append(l[i][0])
    visited[i] = True
    step = int(l[i][1])
    if step == 0:
        break
    i += step
print(''.join(s))

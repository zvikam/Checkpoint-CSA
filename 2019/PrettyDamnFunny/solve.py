import xml.etree.ElementTree as ET


tree = ET.parse('raven.xml')
root = tree.getroot()
characters = {}
for obj in root.findall('object'):
    for data in obj.findall('stream/data'):
        characters[int(obj.attrib['id'])] = data.text[data.text.index('%')+1]

print(characters)

with open('raven.pdf', 'rb') as fin:
    pdf_data = fin.read()

"""
offsets = {}
start = 0
while True:
    offset = pdf_data.find(b' obj', start)
    if offset == -1:
        break
    start = offset + len(b' obj')
    for i in range(offset):
        if pdf_data[offset-1] == ord('\n'):
            break
        offset -= 1
    index = int(pdf_data[offset:start].split()[0])
    offsets[index] = offset
    
print(offsets)
"""

solution = ''
lines = pdf_data.split(b'\n')
for l in lines:
    #offset = pdf_data.find(b'MediaBox', start)
    #if offset == -1:
    #    break
    if l.find(b'MediaBox') > 0:
        solution += characters[int(l.split(b' ')[8])]

print(solution)
    

import sys


exits = [-1] * 16

def find_exit(l):
    print(l, "=============")
    with open('SDLPoP-master/data/LEVELS/res20%02d.bin' % l, 'rb') as fin:
        data = fin.read()

    start = data[2112]
    finish = -1
    
    for r in range(24):
        r_left, r_right, r_up, r_down = data[1952 + r*4:1952 + r*4+4]
        tiles_for = data[0 + r*30:0 + r*30 + 30]
        tiles_bck = data[720 + r*30:720 + r*30 + 30]
        print(r+1, r_left, r_up, r_right, r_down)
        for t in range(30 - 1):
            if (tiles_for[t] & 0x1F) == 0x10 and (tiles_for[t+1] & 0x1F) == 0x11:
                if start != r+1:
                    finish = r+1
    return finish
             

for l in range(16):
    exits[l] = find_exit(l)
print(exits)

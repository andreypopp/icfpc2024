#!/usr/bin/env python

import sys, functools, math, random, itertools

def read():
    ret = []
    for line in sys.stdin.readlines():
        line = line.strip()
        if not line:
            continue
        x, y = line.split(' ')
        ret.append((int(x), int(y)))
    return ret



def sort_key(v):
    return (v[1] < 0, v[0] < 0, abs(v[1]) , abs(v[0]))

def closer_key(v):
    # return sort_key(v) # <- initially problems solved with it
    return abs(v[0]) + abs(v[1])

# sign = functools.partial(math.copysign, 1)
# def sort_key(v):
#     return key(v)

def add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def sub(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])

data = read()
# s = sorted(data, key=sort_key)
s = data
def run(data):
    path = []

    pos = (0, 0)
    v = (0, 0)
    vs = {(-1,-1):'1', (0,-1):'2', (1,-1):'3', (-1,0):'4', (0,0):'5', (1,0):'6', (-1,1):'7', (0,1):'8', (1,1):'9'}
    visited = {(0, 0): True}

    def step_to(target, pos, v):
        # global
        d = sub(target, pos)
        best_pos_d = None
        best_pos = None
        best_v = None
        best_n = None
        for vd, n in vs.items():
            new_v = add(v, vd)
            new_pos = add(pos, new_v)
            new_pos_d = closer_key(sub(target, new_pos))
            if best_pos_d is None or new_pos_d < best_pos_d:
                best_pos_d = new_pos_d
                best_pos = new_pos
                best_v = new_v
                best_n = n
            if new_pos_d == 0:
                break
        # print("pos", pos, "target", target, "d", d,"v", v, "best_pos_d", best_pos_d, "best_pos", best_pos)
        path.append(best_n)
        v = best_v
        pos = best_pos
        visited[best_pos] = True
        return (best_pos_d == 0, pos, v)

    i = 0
    while i < len(s):
        target = s[i]
        if target in visited:
            i += 1
            continue
        reached, pos, v = step_to(target, pos, v)
        if reached:
            i += 1
    return ''.join(path)

m = 18152
print("x")
# ps = list(itertools.permutations(s))
ps = itertools.permutations(reversed(s))

# print("y")
# random.shuffle(ps)
print("z")
for d in ps:
    v = run(s)
    if len(v) < m:
        print("len=",len(v),":",v)
        m = len(v)

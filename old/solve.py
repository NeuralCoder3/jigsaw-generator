from z3 import *
import time
import random

random.seed(0)

# a 5x5 puzzle
# each has 4 sides => connectors

# w,h = 5,5
# edges = 2 # endless
# edges = 20 # 4 => primary rotations
# edges = 6 

w,h = 5,5
# w,h = 7,7
edges = 6

pieces = [
    [0,0,0,0]
    for _ in range(w*h)
]

used_pieces = set()
        
for y in range(h):
    for x in range(w):
        while True:
            idx = y*w+x
            idx_right = y*w+(x+1)%w
            idx_down = ((y+1)%h)*w+x
            right = random.randint(1,edges)
            down = random.randint(1,edges)
            if x < w-1:
                pieces[idx][1] = right
                pieces[idx_right][3] = -right
            if y < h-1:
                pieces[idx][2] = down
                pieces[idx_down][0] = -down
            ok = True
            for rot in range(4):
                rotated = [
                    pieces[idx][(j+rot)%4]
                    for j in range(4)
                ]
                if tuple(rotated) in used_pieces:
                    ok = False
                    break
            if ok:
                used_pieces.add(tuple(rotated))
                break
            
        
# draw the pieces => on edges draw the number
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()
ax.set_xticks(np.arange(0, w, 1))
ax.set_yticks(np.arange(0, h, 1))
for y in range(h):
    for x in range(w):
        idx = y*w+x
        # ax.text(x+0.5, y+0.5, str(pieces[idx]), ha='center', va='center', color='black')
        # offset = 0.25
        offset = 0.15
        # ax.text(x+0.5, y+1-offset, str(pieces[idx][0]), ha='center', va='center', color='black')
        # ax.text(x+0.5, y+offset, str(pieces[idx][2]), ha='center', va='center', color='black')
        ax.text(x+0.5, y+offset, str(pieces[idx][0]), ha='center', va='center', color='black')
        ax.text(x+0.5, y+1-offset, str(pieces[idx][2]), ha='center', va='center', color='black')
        ax.text(x+1-offset, y+0.5, str(pieces[idx][1]), ha='center', va='center', color='black')
        ax.text(x+offset, y+0.5, str(pieces[idx][3]), ha='center', va='center', color='black')
        ax.plot([x,x+1],[y,y], color='black')
        ax.plot([x,x],[y,y+1], color='black')
        ax.plot([x+1,x+1],[y,y+1], color='black')
        ax.plot([x,x+1],[y+1,y+1], color='black')
        
plt.gca().invert_yaxis()
plt.grid()
plt.savefig("puzzle.png")

piece_count = len(pieces)

set_param('parallel.enable', True)

s = Solver()

def exactly_one(args):
    at_least = Or(args)
    # at_most = And([Or(Not(a), Not(b)) for a in args for b in args if a != b])
    at_most = And([Or(Not(a), Not(b)) for i,a in enumerate(args) for b in args[i+1:]])
    return And(at_least, at_most)

positions = [
    [
        [
            Bool(f"pos{i}_{j}_r{k}")
            for k in range(4)
        ]
        for j in range(w*h)
    ]
    for i in range(piece_count)
]

# each piece is at exactly one position
for rot in range(piece_count):
    s.add(exactly_one([
        positions[rot][j][k]
        for j in range(w*h)
        for k in range(4)
    ]))
    
    
# piece 0 is at position 0
s.add(positions[0][0][0])

sides = [
    [Int(f"side{i}_{k}") for k in range(4)] # north, east, south, west
    for i in range(w*h)
]

for i in range(w*h):
    for p in range(piece_count):
        for r in range(4):
            s.add(Implies(positions[p][i][r], And([
                sides[i][k] == pieces[p][(k+r)%4]
                for k in range(4)
            ])))
            
            
for x in range(w):
    idx_up = 0*w+x
    idx_down = (h-1)*w+x
    s.add(sides[idx_up][0] == 0)
    s.add(sides[idx_down][2] == 0)
    
for y in range(h):
    idx_left = y*w+0
    idx_right = y*w+(w-1)
    s.add(sides[idx_left][3] == 0)
    s.add(sides[idx_right][1] == 0)
    
for y in range(h):
    for x in range(w):
        idx = y*w+x
        if x < w-1:
            idx_right = y*w+(x+1)
            s.add(sides[idx][1] == -sides[idx_right][3])
        if y < h-1:
            idx_down = (y+1)*w+x
            s.add(sides[idx][2] == -sides[idx_down][0])
            
t0 = time.time()
res = s.check()
t1 = time.time()

if res == sat:
    m = s.model()
    print(f"There is a solution after {t1-t0:.2f}s")
    
    count = 1
    while True:
        print(f"Solution {count}")
        s.add(Or([
            positions[p][i][r] != m[positions[p][i][r]]
            for p in range(piece_count)
            for i in range(w*h)
            for r in range(4)
        ]))
        res = s.check()
        if res == sat:
            m = s.model()
            count += 1
        else:
            break
else:
    print("No solution found")
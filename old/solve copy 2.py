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

w,h = 7,7
edges = 6

pieces = [
    [0,0,0,0]
    for _ in range(w*h)
]
        
for y in range(h):
    for x in range(w):
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


# pieces = [
#     # (0,1,1,0),
#     # (0,0,1,-1),
#     # (-1,1,0,0),
#     # (-1,0,0,-1),
    
#     (0,1,-1,0),
#     (0,0,1,-1),
#     (1,-1,0,0),
#     (-1,0,0,1),
# ]
piece_count = len(pieces)

set_param('parallel.enable', True)

s = Solver()


rotations = [
    Int(f"rot_{i}")
    for i in range(piece_count)
]

positions = [
    (Int(f"x_{i}"), Int(f"y_{i}"))
    for i in range(piece_count)
]

# w,h = 5,5
# w,h = 2,2

sides = [[
    [Int(f"side_{x}_{y}_{k}") for k in range(4)] # north, east, south, west
    for x in range(w)
] for y in range(h)]


# each border has side 0
for x in range(w):
    s.add(sides[0][x][0] == 0)
    s.add(sides[h-1][x][2] == 0)
    
for y in range(h):
    s.add(sides[y][0][3] == 0)
    s.add(sides[y][w-1][1] == 0)
    
# each side has to be the negative of the side of the neighbor
for y in range(h):
    for x in range(w):
        if x < w-1:
            s.add(sides[y][x][1] == -sides[y][x+1][3])
        if y < h-1:
            s.add(sides[y][x][2] == -sides[y+1][x][0])
            

for y in range(h):
    for x in range(w):
        for p in range(piece_count):
            px,py = positions[p]
            for i in range(4):
                for r in range(4):
                    s.add(Implies(And(px == x, py == y, rotations[p] == r), sides[y][x][i] == pieces[p][(i+r)%4]))
                # s.add(Implies(And(px == x, py == y), sides[y][x][i] == pieces[p][i]))

for p in range(piece_count):
    x,y = positions[p]
    s.add(0 <= rotations[p], rotations[p] < 4)
    s.add(0 <= x, x < w)
    s.add(0 <= y, y < h)
    
# no overlap
for p1 in range(piece_count):
    for p2 in range(p1+1, piece_count):
        x1,y1 = positions[p1]
        x2,y2 = positions[p2]
        s.add(Or(
            x1 != x2,
            y1 != y2
        ))

# fix first piece at 0,0 => no rotations
s.add(positions[0][0] == 0)
s.add(positions[0][1] == 0)
                    
t0 = time.time()
res = s.check()
t1 = time.time()

if res == sat:
    m = s.model()
    print(f"There is a solution after {t1-t0:.2f}s")
    # count solutions
    count = 1
    while True:
        s.add(Or(
            [rotations[i] != m[rotations[i]] for i in range(piece_count)]+
            [positions[i][0] != m[positions[i][0]] for i in range(piece_count)]+
            [positions[i][1] != m[positions[i][1]] for i in range(piece_count)]
        ))
        # remove all 4 total rotations
        res = s.check()
        if res == sat:
            count += 1
            if count % 4 == 1:
                print(f"Solution {count}")
            m = s.model()
        else:
            break
    print(f"Found {count} solutions")
    
    # for y in range(h):
    #     for x in range(w):
    #         print("["+",".join([str(m[pieces[y][x][k]]) for k in range(4)])+"]", end=" ")
    #     print()
else:
    print("no solution")
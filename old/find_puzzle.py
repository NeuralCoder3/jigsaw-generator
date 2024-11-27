from z3 import *
import time

s = Solver()

# a 5x5 puzzle
# each has 4 sides => connectors

w,h = 5,5

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
            

# there is no permutation 


                    
t0 = time.time()
res = s.check()
t1 = time.time()

if res == sat:
    m = s.model()
    for y in range(h):
        for x in range(w):
            print("["+",".join([str(m[sides[y][x][k]]) for k in range(4)])+"]", end=" ")
        print()
else:
    print("no solution")
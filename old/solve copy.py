from z3 import *
import time

s = Solver()

# a 5x5 puzzle
# each has 4 sides => connectors

pieces = [
    # (0,1,1,0),
    # (0,0,1,-1),
    # (-1,1,0,0),
    # (-1,0,0,-1),
    
    (0,1,-1,0),
    (0,0,1,-1),
    (1,-1,0,0),
    (-1,0,0,1),
]
piece_count = len(pieces)

rotations = [
    Int(f"rot_{i}")
    for i in range(piece_count)
]

positions = [
    (Int(f"x_{i}"), Int(f"y_{i}"))
    for i in range(piece_count)
]

# w,h = 5,5
w,h = 2,2

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
    

# there is no permutation 


                    
t0 = time.time()
res = s.check()
t1 = time.time()

if res == sat:
    m = s.model()
    print("There is a solution")
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
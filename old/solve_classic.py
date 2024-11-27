import numba.typed
from z3 import *
import time
import random
import numba
import typing
import numpy as np
import tqdm

# random.seed(0)
random.seed(42)

# a 5x5 puzzle
# each has 4 sides => connectors

# w,h = 5,5
# edges = 2 # endless
# edges = 20 # 4 => primary rotations
# edges = 6 

w,h = 7,7
edges = 6

pieces : typing.List[typing.List[int]] = [
    [0,0,0,0]
    for _ in range(w*h)
]
piece_count = w*h
        
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


# convert pieces to a static const array
pieces = np.array(pieces)
solutions = []

# placed : typing.List[int] = np.zeros((w,h), dtype=np.int32)
# placed : typing.List[int] = [0] * (w*h)
# placed = np.zeros((w,h), dtype=np.int32)

# @numba.jit
def solutions():
    placed = np.zeros((w,h), dtype=np.int32)
    solutions = []
    stack = [(0, 0, list(range(w*h)))]
    while True:
        if len(stack) == 0:
            break
        x, y, remaining = stack.pop()
        if len(remaining) == 0:
            solutions.append(placed.copy())
            print("Solution found", placed)
            continue
        if x >= w:
            x = 0
            y += 1
            stack.append((x, y, remaining))
            continue
        if y >= h:
            continue
        if x > 0:
            side_left = pieces[placed[y,x-1]][1]
        else:
            side_left = 0
        if y > 0:
            side_up = pieces[placed[y-1,x]][2]
        else:
            side_up = 0
        for i, piece in enumerate(remaining):
            if len(remaining) == piece_count and piece != 0:
                continue
            if x > 0 and pieces[piece][3] != -side_left:
                continue
            if y > 0 and pieces[piece][0] != -side_up:
                continue
            placed[y,x] = piece
            new_remaining = remaining[:i] + remaining[i+1:]
            stack.append((x+1, y, new_remaining))
            placed[y,x] = 0
    return len(solutions)
    
    
    # def find(x, y, remaining):
    #     if len(remaining) == 0:
    #         # solutions.append(placed.copy())
    #         print("Solution found", placed)
    #         return 1
    #     if x >= w:
    #         x = 0
    #         y += 1
    #         return find(x, y, remaining)
    #     if y >= h:
    #         return 0
    #     # idx = y*w+x
    #     # idx_left = y*w+(x-1)%w
    #     # idx_up = ((y-1)%h)*w+x
    #     if x > 0:
    #         # sides_left = pieces[placed.flat[idx_left]]
    #         sides_left = pieces[placed[y,x-1]]
    #     if y > 0:
    #         # sides_up = pieces[placed.flat[idx_up]]
    #         sides_up = pieces[placed[y-1,x]]
    #     for i, piece in enumerate(remaining):
    #         if x > 0 and pieces[piece][3] != -sides_left[1]:
    #             continue
    #         if y > 0 and pieces[piece][0] != -sides_up[2]:
    #             continue
    #         # placed.flat[idx] = piece
    #         placed[y,x] = piece
    #         new_remaining = remaining[:i] + remaining[i+1:]
    #         find(x+1, y, new_remaining)
    #         # placed.flat[idx] = 0
    #         placed[y,x] = 0
    # return find(0, 0, list(range(w*h)))

sol_count = solutions()
print("Solutions:", sol_count)
    

# @numba.njit
def solutions(trace: typing.List[int], x : int, y : int, remaining : typing.List[int]):
    # global placed
    if len(remaining) == 0:
        # print("Solution found", placed)
        print("Solution found", trace)
        return 1
    if x >= w:
        x = 0
        y += 1
        return solutions(new_trace, x, y, remaining)
    if y >= h:
        assert False
        # return 0
    idx = y*w+x
    idx_left = y*w+(x-1)%w
    idx_up = ((y-1)%h)*w+x
    if x > 0:
        # sides_left = pieces[placed[idx_left]]
        sides_left = pieces[trace[idx_left]]
    if y > 0:
        # sides_up = pieces[placed[idx_up]]
        sides_up = pieces[trace[idx_up]]
    count = 0
    enum = list(enumerate(remaining))
    # if len(remaining) == piece_count:
    #     enum = [(0, 0)]
    # if len(remaining) == piece_count - 1:
    #     enum = tqdm.tqdm(enum)
    for i, piece in enum:
        if len(remaining) == piece_count and piece != 0:
            continue
        if len(remaining) == piece_count - 1:
            print(f"Piece {i}/{piece_count-1}")
        sides = pieces[piece]
        if x > 0 and sides[3] != -sides_left[1]:
            continue
        if y > 0 and sides[0] != -sides_up[2]:
            continue
        # placed[idx] = piece
        # np.put(placed, idx, piece)
        new_trace = trace + [piece]
        new_remaining = remaining[:i] + remaining[i+1:]
        count += solutions(new_trace, x+1, y, new_remaining)
        # placed[idx] = 0
    return count

# trace : typing.List[int] = []
        
# sol_count = solutions( trace, 0, 0, list(range(w*h)))
# print("Solutions:", sol_count)
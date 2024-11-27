import random
import itertools
from unionfind import unionfind
import sys

random.seed(2)
if len(sys.argv) > 1:
    random.seed(int(sys.argv[1]))

# w,h = 5,5
# w,h = 9,9
w,h = 7,7
if len(sys.argv) > 3:
    w,h = map(int, sys.argv[2:4])

# pieces = [(i,0) for i in  range(w*h)]
# pieces2 = list(random.sample(range(w*h), w*h))
# only shuffle inner pieces

side_indices = [(x,0) for x in range(1,w-1)]+\
    [(x,h-1) for x in range(1,w-1)]+\
    [(0,y) for y in range(1,h-1)]+\
    [(w-1,y) for y in range(1,h-1)]+\
    []

pieces = list(range(w*h))

pieces2 = list(range(w*h))
for indices_to_shuffle in [
    [(x,y) for x in range(1,w-1) for y in range(1,h-1)],
    
    side_indices
    
    # [(x,0) for x in range(1,w-1)],
    # [(x,h-1) for x in range(1,w-1)],
    # [(0,y) for y in range(1,h-1)],
    # [(w-1,y) for y in range(1,h-1)],
]:
    # indices_to_shuffle = [
    #     (x,y) for x in range(1,w-1) for y in range(1,h-1)
    # ]
    shuffled_indices = random.sample(indices_to_shuffle, len(indices_to_shuffle))
    for i, (x,y) in enumerate(indices_to_shuffle):
        x2,y2 = shuffled_indices[i]
        idx = y*w+x
        idx2 = y2*w+x2
        pieces2[idx], pieces2[idx2] = pieces2[idx2], pieces2[idx]
    
    

# shuffle the top row

    
    
pieces3 = [(0,p) for p in pieces2]

for x,y in side_indices:
    idx = y*w+x
    pidx = pieces2[idx]
    px,py = pidx % w, pidx // w
    
    rot = 0
    if y == 0 and py == h-1:
        rot = 2
    if y == 0 and px == 0:
        rot = 3
    if y == 0 and px == w-1:
        rot = 1
        
    if y == h-1 and py == 0:
        rot = 2
    if y == h-1 and px == 0:
        rot = 1
    if y == h-1 and px == w-1:
        rot = 3
        
    if x == 0 and py == h-1:
        rot = 3
    if x == 0 and py == 0:
        rot = 1
    if x == 0 and px == w-1:
        rot = 2
        
    if x == w-1 and py == h-1:
        rot = 1
    if x == w-1 and py == 0:
        rot = 3
    if x == w-1 and px == 0:
        rot = 2
        
    
    pieces3[idx] = (rot, pidx)
    
    


# if we wanna rotate
# for x,y in indices_to_shuffle:
#     idx = y*w+x
#     # pieces3[idx] = (random.randint(0,3), pieces2[idx])
#     pieces3[idx] = (0, pieces2[idx])
#     # pieces3[idx] = (0 if random.random() < 0.9 else 1, pieces2[idx])

# for y in range(h):
#     for x in range(w):
#         idx = y*w+x
#         print(pieces2[idx], end=" ")
#     print()
    
# exit(0)

edges = [
    [0,0,0,0] for i in range(w*h)
]

# print(pieces)
# print(pieces2)

# each piece has 4 edges
offset = 100
u = unionfind(w*h*4+offset)

# side 0: north, 1: east, 2: south, 3: west
def get_index(x,y,side):
    return (y*w+x)*4+side + offset

def get_index_alt(x,y,side):
    idx = y*w+x
    rot, piece_idx = pieces3[idx]
    x,y = piece_idx % w, piece_idx // w
    return get_index(x,y,(side+rot)%4)

# all edges are one set (name (0,0,0))
border_edge = 0
for x in range(w):
    # north edge of border
    u.unite(border_edge, get_index(x,0,0))
    # south edge of border
    u.unite(border_edge, get_index(x,h-1,2))
for y in range(h):
    # west edge of border
    u.unite(border_edge, get_index(0,y,3))
    # east edge of border
    u.unite(border_edge, get_index(w-1,y,1))

# each piece is connected to the next piece
for y in range(h):
    for x in range(w):
        if x < w-1:
            # piece fits to the one on the right
            u.unite(get_index(x,y,1), get_index(x+1,y,3))
            # in alternative configuration, the pieces must fit
            u.unite(get_index_alt(x,y,1), get_index_alt(x+1,y,3))
        if y < h-1:
            # piece fits to the one below
            u.unite(get_index(x,y,2), get_index(x,y+1,0))
            # in alternative configuration, the pieces must fit
            u.unite(get_index_alt(x,y,2), get_index_alt(x,y+1,0))
            
# sides coincide with the alternative in its place
for y in range(h):
    for x in range(w):
        for side in range(4):
            idx = get_index(x,y,side)
            idx_alt = get_index_alt(x,y,side)
            # u.unite(idx, idx_alt)
            
            
            
edge_types = [
    [-1,-1,-1,-1] for _ in range(w*h)
]

number = 0
for y in range(h):
    for x in range(w):
        for side in range(4):
            if edge_types[y*w+x][side] != -1:
                continue
            idx = get_index(x,y,side)
            for y2 in range(h):
                for x2 in range(w):
                    for side2 in range(4):
                        idx2 = get_index(x2,y2,side2)
                        if u.issame(idx, idx2):
                            edge_types[y*w+x][side] = number
                            edge_types[y2*w+x2][side2] = number
            number += 1
            
for y in range(h):
    for x in range(w):
        idx = y*w+x
        idx_down = y*w+(x+1)%w
        idx_right = ((y+1)%h)*w+x
        right_side = 1 if random.random() < 0.5 else -1
        down_side = 1 if random.random() < 0.5 else -1
        if x < w-1:
            edge_types[idx][1] = edge_types[idx][1] * right_side
            edge_types[idx_down][3] = edge_types[idx_down][3] * (-right_side)
        if y < h-1:
            edge_types[idx][2] = edge_types[idx][2] * down_side
            edge_types[idx_right][0] = edge_types[idx_right][0] * (-down_side)
        
        
edge_types2 = []
for y in range(h):
    for x in range(w):
        idx = y*w+x
        rot, piece_idx = pieces3[idx]
        sides = []
        for side in range(4):
            sides.append(edge_types[piece_idx][(side+rot)%4])
        edge_types2.append(sides)
            
# print(edge_types)

with open("puzzle.txt","w") as f:
    f.write(f"{w} {h}\n")
    f.write("\n")
    for y in range(h):
        for x in range(w):
            idx = y*w+x
            f.write(f"{idx},0: ")
            for side in range(4):
                f.write(f"{edge_types[idx][side]} ")
            f.write("\n")
        f.write("\n")
    
with open("puzzle2.txt","w") as f:
    f.write(f"{w} {h}\n")
    f.write("\n")
    for y in range(h):
        for x in range(w):
            idx = y*w+x
            rot, piece_idx = pieces3[idx]
            f.write(f"{piece_idx},{rot}: ")
            for side in range(4):
                f.write(f"{edge_types2[idx][side]} ")
            f.write("\n")
        f.write("\n")

# def draw_puzzle(pieces, w, h, filename="puzzle.png"):
#     import matplotlib.pyplot as plt
#     import numpy as np

#     fig, ax = plt.subplots()
#     ax.set_xticks(np.arange(0, w, 1))
#     ax.set_yticks(np.arange(0, h, 1))
#     for y in range(h):
#         for x in range(w):
#             idx = y*w+x
#             # ax.text(x+0.5, y+0.5, str(pieces[idx]), ha='center', va='center', color='black')
#             # offset = 0.25
#             offset = 0.15
#             # ax.text(x+0.5, y+1-offset, str(pieces[idx][0]), ha='center', va='center', color='black')
#             # ax.text(x+0.5, y+offset, str(pieces[idx][2]), ha='center', va='center', color='black')
#             ax.text(x+0.5, y+offset, str(pieces[idx][0]), ha='center', va='center', color='black')
#             ax.text(x+0.5, y+1-offset, str(pieces[idx][2]), ha='center', va='center', color='black')
#             ax.text(x+1-offset, y+0.5, str(pieces[idx][1]), ha='center', va='center', color='black')
#             ax.text(x+offset, y+0.5, str(pieces[idx][3]), ha='center', va='center', color='black')
#             ax.plot([x,x+1],[y,y], color='black')
#             ax.plot([x,x],[y,y+1], color='black')
#             ax.plot([x+1,x+1],[y,y+1], color='black')
#             ax.plot([x,x+1],[y+1,y+1], color='black')
            
#     plt.gca().invert_yaxis()
#     plt.grid()
#     plt.savefig(filename)
    
# draw_puzzle(edge_types, w, h, "puzzle.png")
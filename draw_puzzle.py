import matplotlib.pyplot as plt
import numpy as np
import sys

infile = "puzzle.txt"
# output = "puzzle.png"
output = "puzzle.svg"

if len(sys.argv) > 2:
    infile = sys.argv[1]
    output = sys.argv[2]
    

identity = []

with open(infile) as f:
    w, h = map(int, f.readline().strip().split())
    f.readline()
    pieces = []
    for y in range(h):
        for x in range(w):
            line = f.readline().strip()
            info, sides = line.split(":")
            idx, rot = map(int, info.split(","))
            sides = list(map(int, sides.strip().split()))
            
            pieces.append(list(map(int, sides)))
            identity.append((idx, rot))
        f.readline()
        
svg = False
if output.endswith(".svg"):
    svg = True

fig, ax = plt.subplots()
ax.set_xticks(np.arange(0, w, 1))
ax.set_yticks(np.arange(0, h, 1))

# smaller font size
plt.rcParams.update({'font.size': 8})

from jigsaw_bezier import *
for y in range(h):
    for x in range(w):
        idx = y*w+x
        # draw_bezier_segments(ax,b_set, scale=0.01)
        
        # if x < w-1:
        side = pieces[idx][1]
        flipped = False
        if side < 0:
            flipped = True
            side = -side
        b_set = make_beziers(seed=side, offset=10)
        if flipped:
            b_set = mirror(b_set, sign_y=-1)
        # b_set = mirror(b_set, sign_y=-1)
        b_set = rotate(b_set)
        rightside=draw_bezier_segments(ax, b_set, offset_x=x+1, offset_y=y+1, scale=0.01)
        
        
        # if y < h-1:
        side = pieces[idx][2]
        flipped = False
        if side < 0:
            flipped = True
            side = -side
        b_set = make_beziers(seed=side, offset=10)
        if flipped:
            b_set = mirror(b_set, sign_y=-1)
        downside=draw_bezier_segments(ax, b_set, offset_x=x, offset_y=y+1, scale=0.01)
        
        
        upside = pieces[idx][0]
        uflipped = upside < 0
        upside = abs(upside)
        upside = make_beziers(seed=upside, offset=10)
        if not uflipped:
            upside = mirror(upside, sign_y=-1)
        upside = draw_bezier_segments(None, upside, offset_x=x, offset_y=y, scale=0.01, color="red")
        
        leftside = pieces[idx][3]
        lflipped = leftside < 0
        leftside = abs(leftside)
        leftside = make_beziers(seed=leftside, offset=10)
        if not lflipped:
            leftside = mirror(leftside, sign_y=-1)
        leftside = rotate(leftside)
        leftside = draw_bezier_segments(None, leftside, offset_x=x, offset_y=y+1, scale=0.01, color="red")
            
        # fill the closed curve with a color
        # curve = np.concatenate([upside, rightside, downside, leftside])
        
        # upside = np.flipud(upside)
        rightside = np.flipud(rightside)
        downside = np.flipud(downside)
        # leftside = np.flipud(leftside)
        # if lflipped:
        #     leftside = np.flipud(leftside)
        curve = np.concatenate([upside,rightside,downside,leftside])
        id, rot = identity[idx]
        ix,iy = id%w, id//w
        if not svg:
            ax.fill(curve[:,0], curve[:,1], color=(ix/w, iy/h, 0.5), alpha=0.5)
        
        
        
        
        offset = 0.15
        if not svg:
            ax.text(x+0.5, y+offset, str(pieces[idx][0]), ha='center', va='center', color='black')
            ax.text(x+0.5, y+1-offset, str(pieces[idx][2]), ha='center', va='center', color='black')
            ax.text(x+1-offset, y+0.5, str(pieces[idx][1]), ha='center', va='center', color='black')
            ax.text(x+offset, y+0.5, str(pieces[idx][3]), ha='center', va='center', color='black')
            
            # draw a colored rectangle (x as green and y as red) 
            # ax.add_patch(plt.Rectangle((x, y), 1, 1, fill=True, color=(ix/w, iy/h, 0.5), alpha=0.5))
            ax.text(x+0.5, y+0.5, f"{id},{rot}", ha='center', va='center', color='blue')
            
            
        
        # ax.plot([x,x+1],[y,y], color='black')
        # ax.plot([x,x],[y,y+1], color='black')
        # ax.plot([x+1,x+1],[y,y+1], color='black')
        # ax.plot([x,x+1],[y+1,y+1], color='black')
        
        if x == 0:
            ax.plot([x,x],[y,y+1], color='black')
        if y == 0:
            ax.plot([x,x+1],[y,y], color='black')
        # if x == w-1:
        #     ax.plot([x+1,x+1],[y,y+1], color='black')
        # if y == h-1:
        #     ax.plot([x,x+1],[y+1,y+1], color='black')
            
            
            
        

# for y in range(h):
#     for x in range(w):
#         idx = y*w+x
#         # ax.text(x+0.5, y+0.5, str(pieces[idx]), ha='center', va='center', color='black')
#         # offset = 0.25
#         offset = 0.15
#         # ax.text(x+0.5, y+1-offset, str(pieces[idx][0]), ha='center', va='center', color='black')
#         # ax.text(x+0.5, y+offset, str(pieces[idx][2]), ha='center', va='center', color='black')
#         ax.text(x+0.5, y+offset, str(pieces[idx][0]), ha='center', va='center', color='black')
#         ax.text(x+0.5, y+1-offset, str(pieces[idx][2]), ha='center', va='center', color='black')
#         ax.text(x+1-offset, y+0.5, str(pieces[idx][1]), ha='center', va='center', color='black')
#         ax.text(x+offset, y+0.5, str(pieces[idx][3]), ha='center', va='center', color='black')
#         ax.plot([x,x+1],[y,y], color='black')
#         ax.plot([x,x],[y,y+1], color='black')
#         ax.plot([x+1,x+1],[y,y+1], color='black')
#         ax.plot([x,x+1],[y+1,y+1], color='black')
        
# plt.gca().invert_yaxis()
plt.gcf().set_size_inches(w, h)
if svg:
    # deactivate the coordinate grid
    ax.axis('off')
else:
    # plt.grid()
    ax.axis('off')
    pass
plt.savefig(output)
# plt.show()
# plt.savefig("test.svg")
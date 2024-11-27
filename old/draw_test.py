import matplotlib.pyplot as plt

import numpy as np
from scipy.special import comb
import matplotlib.patches as mpatches
import matplotlib.path as mpath

# bezier curve
def B(i, N, t):
    val = comb(N,i) * t**i * (1.-t)**(N-i)
    return val
def P(t, X):
    '''
     xx = P(t, X)
     
     Evaluates a Bezier curve for the points in X.
     
     Inputs:
      X is a list (or array) or 2D coords
      t is a number (or list of numbers) in [0,1] where you want to
        evaluate the Bezier curve
      
     Output:
      xx is the set of 2D points along the Bezier curve
    '''
    X = np.array(X)
    N,d = np.shape(X)   # Number of points, Dimension of points
    N = N - 1
    xx = np.zeros((len(t), d))
    
    for i in range(N+1):
        xx += np.outer(B(i, N, t), X[i])
    
    return xx

coords = [
    (0,0),
    (2,0),
    (2,1),
    (1,1),
    (1,2),
    (4,2),
    (4,1),
    (3,1),
    (3,0),
    (5,0),
]


tt = np.linspace(0, 1, 200)
X = np.array(coords)
xx = P(tt, coords)

plt.plot(xx[:,0], xx[:,1])
plt.plot(X[:,0], X[:,1], 'ro')    

plt.show()

# draw bezier curve with control points
# x = [c[0] for c in coords]
# y = [c[1] for c in coords]

# fig, ax = plt.subplots()

# # plt.plot(x, y, 'ro')
# # plt.plot(x, y, 'b-')
# # ax.plot(x, y, 'b-')
# ax.plot(x, y, 'ro')

# Path = mpath.Path
# # pp1 = mpatches.PathPatch(
# #     Path([(0, 0), (1, 0), (1, 1), (0, 0)],
# #          [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.CLOSEPOLY]),
# #     fc="none", transform=ax.transData)
# pp1 = mpatches.PathPatch(
#     Path(coords, [Path.MOVETO] + [Path.CURVE3] * (len(coords)-2) + [Path.MOVETO]),
#     fc="none", transform=ax.transData)

# ax.add_patch(pp1)

# plt.show()
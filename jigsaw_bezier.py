import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb  
import random

def bezier_curve(control_points, num_points=200):
    """
    Generate a Bézier curve from control points.
    """
    t = np.linspace(0, 1, num_points)
    n = len(control_points) - 1
    curve = np.zeros((num_points, 2))
    
    for i, point in enumerate(control_points):
        bernstein = comb(n, i) * (t ** i) * ((1 - t) ** (n - i))
        curve += np.outer(bernstein, point)
    
    return curve


def draw_bezier_segments(plt,beziers, offset_x=0, offset_y=0, scale=1, color_map=None, debug=False, dashed=False, color="black"):
    """
    Draw Bézier segments based on control points.
    """
    start_point = np.array([offset_x, offset_y])  # Starting point
    if color_map is None:
        color_map = ['red', 'green', 'blue', 'gold', 'purple', 'cyan']

    all_points = []
    curves = []
    for i, b in enumerate(beziers):
        # Define control points for the current Bézier curve
        control_points = [
            (start_point[0] + b['cx1'] * scale, start_point[1] + b['cy1'] * scale),
            (start_point[0] + b['cx2'] * scale, start_point[1] + b['cy2'] * scale),
            (start_point[0] + b['ex'] * scale, start_point[1] + b['ey'] * scale),
        ]
        all_points.extend(control_points)
        
        # Generate the Bézier curve
        curve = bezier_curve(control_points)
        curves.append(curve)

        # Plot the curve
        if debug and plt is not None:
            plt.plot(curve[:, 0], curve[:, 1], color=color_map[i % len(color_map)], linewidth=2)
        # else:
        #     # plt.plot(curve[:, 0], curve[:, 1], color="black", linewidth=2)
        #     if dashed:
        #         plt.plot(curve[:, 0], curve[:, 1], color="black", linestyle='dashed', linewidth=1)
        #     else:
        #         plt.plot(curve[:, 0], curve[:, 1], color="black", linewidth=2)

        # Update the start point for the next segment
    curves = np.concatenate(curves)
    # from scipy.interpolate import make_interp_spline
    # x = curves[:, 0]
    # y = curves[:, 1]
    # phi = np.linspace(0, 2*np.pi, len(x))
    # spl = make_interp_spline(phi, np.c_[x, y])
    # phi_new = np.linspace(0, 2.*np.pi, 100)
    # x_new, y_new = spl(phi_new).T
    # curves = np.c_[x_new, y_new]
    # ynew = spl(xnew)
    # # curves[:, 1] = ynew
    # plt.plot(xnew, ynew, color="black", linewidth=2)
    
    if not debug and plt is not None:
        if dashed:
            plt.plot(curves[:, 0], curves[:, 1], color=color, linestyle='dashed', linewidth=1)
        else:
            plt.plot(curves[:, 0], curves[:, 1], color=color, linewidth=2)
        
    if debug and plt is not None:
        plt.scatter([p[0] for p in all_points], [p[1] for p in all_points], color='black', s=10)
        
    return curves
    


def mirror(beziers, sign_x=1, sign_y=1, offset_x=0, offset_y=0):
    """
    Mirror Bézier control points along the x or y axis.
    """
    mirrored = []
    for b in beziers:
        mirrored.append({
            'cx1': b['cx1'] * sign_x + offset_x,
            'cy1': b['cy1'] * sign_y + offset_y,
            'cx2': b['cx2'] * sign_x + offset_x,
            'cy2': b['cy2'] * sign_y + offset_y,
            'ex': b['ex'] * sign_x + offset_x,
            'ey': b['ey'] * sign_y + offset_y,
        })
    return mirrored

def transpose(beziers):
    transposed = []
    for b in beziers:
        transposed.append({
            'cx1': b['cy1'],
            'cy1': b['cx1'],
            'cx2': b['cy2'],
            'cy2': b['cx2'],
            'ex': b['ey'],
            'ey': b['ex'],
        })
    return transposed
    
def rotate(beziers):
    # return transpose(mirror(beziers, sign_x=-1, sign_y=1))
    return mirror(transpose(beziers), sign_x=1, sign_y=-1)
    

def make_beziers(seed=42, offset=5):
    """
    Define the original Bézier segments.
    """
    p = [
        (0, 0),
        (37, 5),
        (38, -5),
        (50, -20),
        (62, -5),
        (63, 5),
        (100, 0),
    ]
    c = [
        (35, 15),
        (40, 0),
        (20, -20),
        (80, -20),
        (60, 0),
        (65, 15),
    ]
    
    # adjust the control points a little bit
    offset = 5
    random.seed(seed)
    for i in range(1, 6):
        c[i] = (c[i][0] + random.randint(-offset, offset), c[i][1] + random.randint(-offset, offset))
    
    
    points = []
    for i in range(6):
        points.append({
            'cx1': p[i][0], 'cy1': p[i][1],
            'cx2': c[i][0], 'cy2': c[i][1],
            'ex': p[i + 1][0], 'ey': p[i + 1][1],
        })
        
    if seed == 0:
        return [
            {'cx1': 0, 'cy1': 0, 'cx2': 50, 'cy2': 0, 'ex': 100, 'ey': 0},
        ]
        
    return mirror(points, sign_x=1, sign_y=-1, offset_x=0, offset_y=0)
    
    
    # p1x,p1y = (0,0)
    # p2x,p2y = (37, 5)
    # p3x,p3y = (38, -5)
    # p4x,p4y = (50, -20)
    # p5x,p5y = (62, -5)
    # p6x,p6y = (63, 5)
    # p7x,p7y = (100, 0)
    
    # c1x,c1y = (35,15)
    # c2x,c2y = (40,0)
    # c3x,c3y = (20,-20)
    # c4x,c4y = (80,-20)
    # c5x,c5y = (60,0)
    # c6x,c6y = (65,15)
    
    # return [
    #     {'cx1': p1x, 'cy1': p1y, 'cx2': c1x, 'cy2': c1y, 'ex': p2x, 'ey': p2y},   # left shoulder
    #     {'cx1': p2x, 'cy1': p2y, 'cx2': c2x, 'cy2': c2y, 'ex': p3x, 'ey': p3y},  # left neck
    #     {'cx1': p3x, 'cy1': p3y, 'cx2': c3x, 'cy2': c3y, 'ex': p4x, 'ey': p4y}, # left head
    #     {'cx1': p4x, 'cy1': p4y, 'cx2': c4x, 'cy2': c4y, 'ex': p5x, 'ey': p5y},  # right head
    #     {'cx1': p5x, 'cy1': p5y, 'cx2': c5x, 'cy2': c5y, 'ex': p6x, 'ey': p6y},   # right neck
    #     {'cx1': p6x, 'cy1': p6y, 'cx2': c6x, 'cy2': c6y, 'ex': p7x, 'ey': p7y},   # right shoulder
    # ]
    
    # return [
    #     {'cx1': 0,  'cy1': 0,  'cx2': 35, 'cy2': 15, 'ex': 37, 'ey': 5},   # left shoulder
    #     {'cx1': 37, 'cy1': 5,  'cx2': 40, 'cy2': 0,  'ex': 38, 'ey': -5},  # left neck
    #     {'cx1': 38, 'cy1': -5, 'cx2': 20, 'cy2': -20, 'ex': 50, 'ey': -20}, # left head
    #     {'cx1': 50, 'cy1': -20, 'cx2': 80, 'cy2': -20, 'ex': 62, 'ey': -5},  # right head
    #     {'cx1': 62, 'cy1': -5, 'cx2': 60, 'cy2': 0,  'ex': 63, 'ey': 5},   # right neck
    #     {'cx1': 63, 'cy1': 5,  'cx2': 65, 'cy2': 15, 'ex': 100, 'ey': 0},   # right shoulder
    # ]


# # Create original and mirrored Bézier sets
# b_set = make_beziers()
# # b_set_mirrored = mirror(b_set, sign_x=1, sign_y=-1)
# # b_set = transpose(b_set)
# b_set = rotate(b_set)

# # Draw the Bézier curves
# plt.figure(figsize=(12, 6))
# draw_bezier_segments(b_set, offset_x=50, offset_y=100, scale=2)
# # draw_bezier_segments(b_set_mirrored, offset_x=50, offset_y=200, scale=2)

# # Finalize the plot
# plt.axis('equal')
# plt.show()

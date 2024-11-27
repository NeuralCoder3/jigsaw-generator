import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb  # Ensure this is imported

def bezier_curve(control_points, num_points=100):
    """
    Calculate a Bézier curve from control points.
    """
    t = np.linspace(0, 1, num_points)
    n = len(control_points) - 1
    curve = np.zeros((num_points, 2))
    for i, (px, py) in enumerate(control_points):
        binomial_coeff = comb(n, i)
        curve[:, 0] += binomial_coeff * (t**i) * ((1 - t)**(n - i)) * px
        curve[:, 1] += binomial_coeff * (t**i) * ((1 - t)**(n - i)) * py
    return curve

def draw_bezier_segments(beziers, offset_x=0, offset_y=0, scale=1, color_map=None):
    start_point = np.array([offset_x, offset_y])  # Starting point
    if color_map is None:
        color_map = ['red', 'green', 'blue', 'gold', 'purple', 'cyan']

    for i, b in enumerate(beziers):
        # Construct Bézier curve using the current start point and control points
        control_points = [
            tuple(start_point),
            (start_point[0] + b['cx1'], start_point[1] + b['cy1']),
            (start_point[0] + b['cx2'], start_point[1] + b['cy2']),
            (start_point[0] + b['ex'], start_point[1] + b['ey']),
        ]
        curve = bezier_curve(control_points)

        # Plot the curve
        plt.plot(curve[:, 0], curve[:, 1], color=color_map[i % len(color_map)], linewidth=2)

        # Update the start point for the next segment
        start_point = np.array([control_points[-1][0], control_points[-1][1]])


def make_beziers():
    """
    Define a set of Bézier control points for a jigsaw piece.
    """
    return [
        {'cx1': 0, 'cy1': 0, 'cx2': 35, 'cy2': 15, 'ex': 37, 'ey': 5},   # left shoulder
        {'cx1': 37, 'cy1': 5, 'cx2': 40, 'cy2': 0, 'ex': 38, 'ey': -5},  # left neck
        {'cx1': 38, 'cy1': -5, 'cx2': 20, 'cy2': -20, 'ex': 50, 'ey': -20}, # left head
        {'cx1': 50, 'cy1': -20, 'cx2': 80, 'cy2': -20, 'ex': 62, 'ey': -5}, # right head
        {'cx1': 62, 'cy1': -5, 'cx2': 60, 'cy2': 0, 'ex': 63, 'ey': 5},   # right neck
        {'cx1': 63, 'cy1': 5, 'cx2': 65, 'cy2': 15, 'ex': 100, 'ey': 0},  # right shoulder
    ]

def mirror(beziers, sign_x=1, sign_y=1, offset_x=0, offset_y=0):
    """
    Mirror Bézier control points across axes and apply translation.
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

# Main execution
beziers = make_beziers()
mirrored_beziers = mirror(beziers, 1, -1)

plt.figure(figsize=(8, 6))
draw_bezier_segments(beziers, offset_x=50, offset_y=100, scale=1.0)
draw_bezier_segments(mirrored_beziers, offset_x=50, offset_y=200, scale=1.0)

plt.axis('equal')
plt.show()

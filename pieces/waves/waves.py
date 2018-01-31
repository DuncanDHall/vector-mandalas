""" A experimental piece for testing the code from this repo. """
from vector_mandalas import bezier
from typing import Tuple


def gen_circle(center: Tuple[int, int], r: int) -> bezier.Path:
    """ Creates an approximation of a circle with four bezier curves using
        calculations from here: http://spencermortensen.com/articles/bezier-circle/

    Args:
        center (Tuple[int]): center point of the circle (x, y)
        r (int): radius of the circle
    """
    c = 0.55191502449  # special number that minimizes deviation from circle
    circle_template = [  # these are in order: endpoint 1 & 2, control 1 & 2
        [(0, -1), (1, 0), (c, -1), (1, -c)],
        [(1, 0), (0, 1), (1, c), (c, 1)],
        [(0, 1), (-1, 0), (-c, 1), (-1, c)],
        [(-1, 0), (0, -1), (-1, -c), (-c, -1)]
    ]

    curves = []
    for curve_template in circle_template:
        curve_points = [
            bezier.Point(int(round(p[0]*r + center[0])), int(round(p[1]*r + center[1])))
            for p in curve_template
        ]

        curves.append(bezier.CubicBezierCurve(*curve_points))

    return bezier.Path(curves)

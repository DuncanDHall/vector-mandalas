""" A experimental piece for testing the code from this repo. """
from __future__ import division

from vector_mandalas import bezier
from typing import Tuple, List


def gen_circle(center: Tuple[float, float], r: float) -> bezier.Path:
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
            (p[0]*r + center[0], p[1]*r + center[1])
            for p in curve_template
        ]

        curves.append(bezier.CubicBezierCurve(*curve_points))

    return bezier.Path(curves)


def split_curve(curve: bezier.CubicBezierCurve, splits: List[float]) -> List[bezier.CubicBezierCurve]:
    """ Splits a bezier curve into two or more sub curves which trace the same
        path (with some rounding)

    Args:
        curve (bezier.CubicBezierCurve): original curve to be split
        splits List(float): a list set of values between 0.0 and 1.0 where splits
            should occur along the curve (not directly correlated with length)
    """
    # TODO:
    return [curve]

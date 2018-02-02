""" A experimental piece for testing the code from this repo. """
from __future__ import division
from typing import Tuple, List

import numpy as np

from vector_mandalas.bezier import CubicBezierCurve, Point, Path


def gen_circle(center: Tuple[float, float], r: float) -> Path:
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

        curves.append(CubicBezierCurve(*curve_points))

    return Path(curves)


def intermediate_point(p1: Point, p2: Point, s: float) -> Point:
    """ Calculates the collinear point proportionally between p1 and p2 with ratio r

    Args:
        p1 (Point): first point (s = 0.0)
        p2 (Point): second point (s = 1.0)
        s (float): the ratio between 0.0 and 1.0 inclusive to use
    """
    x = p1[0] * (1.0 - s) + p2[0] * s
    y = p1[1] * (1.0 - s) + p2[1] * s
    return x, y


def split_curve(curve: CubicBezierCurve, splits: List[float]) -> List[CubicBezierCurve]:
    """ Splits a bezier curve into two or more sub curves which trace the same
        path (with some rounding)

    Args:
        curve (CubicBezierCurve): original curve to be split
        splits (List[float]): a list set of values between 0.0 and 1.0 where splits
            should occur along the curve (not directly correlated with length)
    """
    if not splits:
        return [curve]

    s = splits[0]
    rest_splits = list(map(lambda x: (x-s)/(1-s), splits[1:]))

    m0: Point = intermediate_point(curve.p0, curve.c0, s)
    m1: Point = intermediate_point(curve.c0, curve.c1, s)
    m2: Point = intermediate_point(curve.c1, curve.p1, s)

    q0: Point = intermediate_point(m0, m1, s)
    q1: Point = intermediate_point(m1, m2, s)

    e: Point = intermediate_point(q0, q1, s)

    first_curve = CubicBezierCurve(curve.p0, e, m0, q0)
    rest_curve = CubicBezierCurve(e, curve.p1, q1, m2)

    return [first_curve] + split_curve(rest_curve, rest_splits)


def vary_point(
        point: Point, p: float, max_distance: float, reference_point: Point = None, reference_factor: float = 0.0
) -> Point:
    """ Varies the first input point with probability p and outputs a second
        Point. The point's variation can be skewed towards the reference using
        the reference_factor.

    Args:
        point (Point): point to be varied
        p (float): probability of a variation occuring (ranges 0.0 <= p <= 1.0)
        max_distance (float): max distance to vary the point
        reference_point (Point): the target direction for skewing the variation
        reference_factor (float): degree of skew toward the reference_point
            (ranges 0.0 <= reference_factor <= 1.0)
    """
    if p > 1.0:
        raise ValueError("p must be a probability on the closed interval [0.0, 1.0]")
    if reference_factor > 1.0:
        raise ValueError("reference_factor must be a probability on the closed interval [0.0, 1.0]")

    if np.random.random() >= p:
        return point

    theta: float = (np.random.random() * 2 - 1) * np.pi * (1.0 - reference_factor)
    if reference_point is not None:
        theta += np.arctan2(reference_point[1] - point[1], reference_point[0] - point[0])

    distance: float = np.random.random() * max_distance

    nx: float = np.cos(theta) * distance + point[0]
    ny: float = np.sin(theta) * distance + point[1]
    return nx, ny

"""
.. module:: bezier
    :platform: OS X
    :synopsis: module for creation of bezier paths and export to SVG files

.. moduleauthor:: Duncan Hall
"""

from __future__ import division
from typing import List, Tuple

import numpy as np

Point = Tuple[float, float]


##############################
# Basic Objects              #
##############################


# class Point:  # Deprecated
#     """ Describes a point in 2D cartesian space """
#     def __init__(self, x: int, y: int) -> None:
#         """ Initialization of each dimension
#         Args:
#             x (int): int value for horizontal dimension (higher values right)
#             y (int): int value or vertical dimension (higher values bottom)
#         """
#         self.x = x
#         self.y = y
#
#     def copy(self):  # -> Point
#         """ Returns a copy of this object with optional x and y offset """
#         return Point(self.x, self.y)
#
#     def __eq__(self, o: object) -> bool:
#         """ Allow __eq__ for point comparison """
#         if isinstance(o, Point):
#             return self.x == o.x and self.y == o.y
#         return super().__eq__(o)


class CubicBezierCurve:
    """ Describes a cubic bezier curve with two endpoints
        and two control points """
    def __init__(self, p1: Point, p2: Point, c1: Point = None, c2: Point = None) -> None:
        """ Initialization of each point
        Args:
            p1 (Point): first endpoint
            p2 (Point): second endpoint
            c1 (Point): first control point (defaults to p1)
            c2 (Point): second control point (defaults to p2)
        """
        self.p1 = p1
        self.p2 = p2
        self.c1 = c1 if c1 is not None else p1
        self.c2 = c2 if c2 is not None else p2


class Path(List[CubicBezierCurve]):
    """ A collection of connected bezier curves. This class also includes
        methods for construction and addition of curves to the path. Note
        that this path is ordered.

        Right now this is literally a list, but there may be more specific
        functionality called for in the future. It would also be really
        nice to be able to specify a type hint here... """
    @classmethod
    def from_floats(cls, *floats):
        """ Alternate initializer for compact input of coordinates """
        curves = []
        for i in range(0, len(floats) - 2, 6):
            p1 = (floats[i], floats[i + 1])
            c1 = (floats[i + 2], floats[i + 3])
            c2 = (floats[i + 4], floats[i + 5])
            p2 = (floats[i + 6], floats[i + 7])
            curves.append(CubicBezierCurve(p1, p2, c1, c2))
        return cls(curves)


##############################
# Functions                  #
##############################


def assert_continuous(*curves: CubicBezierCurve) -> bool:
    """ Compares each curve with the next to verify continuity. Note that this
        function treats curves as directed, thus two curves that start at the
        same point will return `False` when compared.

        Args:
            *curves (CubicBezierCurve): the curves to compare
    """
    if not curves:
        raise ValueError("CurveChecker.assert_continuous() cannot be called on an empty list")

    previous_curve = curves[0]
    for curve in curves[1:]:
        if previous_curve.p2 != curve.p1:
            return False
        previous_curve = curve
    return True


def assert_collinear(*points: Point, tolerance: float = 1e-2) -> bool:
    """ Verifies that the adjacent slopes between points are within specified
        tolerance of one another. Note that assert_collinear assumes ordered
        points; three actually collinear points passed with the middle point as
        the first or last argument will return `False`

        Much appreciation to phrogz.net/angle-between-three-points for the
        method of angle calculation.

    Args:
        *points (Point): the points to be compared
        tolerance (float): the error tolerance in radians between adjacent
            slopes (defaults to 0.01)
    """
    if len(points) < 3:
        raise ValueError("CurveChecker.assert_collinear() must be called with at least three points")

    for p1, p2, p3 in zip(points, points[1:], points[2:]):
        d12 = np.hypot(p1[0]-p2[0], p1[1]-p2[1])
        d23 = np.hypot(p2[0]-p3[0], p2[1]-p3[1])
        d31 = np.hypot(p3[0]-p1[0], p3[1]-p1[1])

        theta = np.arccos(0.5 * (d12/d23 + d23/d12 - d31**2/(d12*d23)))
        if np.pi - theta > tolerance:
            return False

    return True


def assert_differentiable(*curves: CubicBezierCurve) -> bool:
    """ Verifies differentiability of curves by checking collinearity of adjacent
        curves' control points

    Args:
        *curves (CubicBezierCurve): curves to be compared
    """
    if not curves:
        raise ValueError("CurveChecker.assert_differentiable() cannot be called on an empty list")

    if not assert_continuous(*curves):
        return False

    for curve1, curve2 in zip(curves, curves[1:]):
        if not assert_collinear(curve1.c2, curve2.p1, curve2.c1):
            return False
    return True


def path_to_string(path: Path) -> str:
    """ Converts a path to a string representation for inclusion in an SVG file as
        described here: https://www.w3.org/TR/SVG11/paths.html

        Verifies that the path is continuous.

        Args:
            path (List[CubicBezierCurve]): path to convert
    """
    assert_continuous(path)

    pieces = ["M {} {}".format(path[0].p1[0], path[0].p1[1])]
    for curve in iter(path):  # iter cast not strictly necessary
        piece = "C {} {} {} {} {} {}".format(
            int(round(curve.c1[0])), int(round(curve.c1[1])),
            int(round(curve.c2[0])), int(round(curve.c2[1])),
            int(round(curve.p2[0])), int(round(curve.p2[1]))
        )
        pieces.append(piece)

    return " ".join(pieces)


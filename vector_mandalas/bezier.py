"""
.. module:: vector_mandalas
    :platform: OS X
    :synopsis: module for creation of cool vector graphics

.. moduleauthor:: Duncan Hall
"""


class Point:
    """ Describes a point in 2D cartesian space """
    def __init__(self, x: float, y: float):
        """ Initialization of each dimension
        Args:
            x (float): float value for horizontal dimension (higher values right)
            y (float): float value or vertical dimension (higher values bottom)
        """
        self.x = x
        self.y = y


class QuadraticBezierCurve:
    """ Describes a quadratic bezier curve with two endpoints
        and two control points """
    def __init__(self, p1: Point, p2: Point, c1: Point = None, c2: Point = None):
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
        self.c2 = c2 if c2 is not None else c2


class Path:
    """ A collection of connected bezier curves. This class also includes
        methods for construction and addition of curves to the path. """
    def __init__(self, curves: [QuadraticBezierCurve] = None):
        """ Initialization of a list of bezier curves

        Args:
            curves ([QuadraticBezierCurve]): curves included in the path (defaults to empty)
        """
        self.curves = curves if curves is not None else []


class SVGPathConverter:
    """ Used to create an SVG11 string representation of a path as
        described here: https://www.w3.org/TR/SVG11/paths.html """

    @staticmethod
    def path_to_string(path):
        """ Converts a path to a string representation for inclusion in an SVG file """
        # TODO
        return ""

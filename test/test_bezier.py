import unittest
from vector_mandalas.bezier import *


class TestPoint(unittest.TestCase):
    """ Point tests """
    def test_1(self):
        """ Point creation """
        p = Point(10, 20)
        self.assertEqual(10, p.x)
        self.assertEqual(20, p.y)

    def test_2(self):
        """ Point Copying """
        p1 = Point(1, 2)
        p2 = p1.copy()
        self.assertIsNot(p1, p2)

        p3 = p1.copy(2, 2)
        self.assertEqual(3, p3.x)
        self.assertEqual(4, p3.y)


class TestCubicBezierCurve(unittest.TestCase):
    """ Cubic bezier curve tests """
    def setUp(self):
        self.start = Point(10, 10)
        self.end = Point(30, 10)
        self.cp1 = Point(10, 30)
        self.cp2 = Point(30, 30)

    def test_1(self):
        """ Line creation """
        linear_curve = CubicBezierCurve(self.start, self.end)

    def test_2(self):
        """ Quadratic curve creation """
        quadratic_curve = CubicBezierCurve(self.start, self.end, self.cp1, self.cp1)

    def test_3(self):
        """ Cubic curve creation """
        cubic_curve = CubicBezierCurve(self.start, self.end, self.cp1, self.cp2)


class TestPath(unittest.TestCase):
    """ Bezier Path tests """
    pass


class TestCurveChecker(unittest.TestCase):
    """ CurveChecker tests """
    def setUp(self):
        self.reference = CubicBezierCurve(
            Point(10, 30), Point(30, 30),
            Point(10, 10), Point(30, 10)
        )  # reference

    def test_1(self):
        """ Test assert_continuous """
        discountinuous_curve = CubicBezierCurve(
            Point(30, 40), Point(10, 60),
            Point(30, 60), Point(30, 60)
        )
        self.assertFalse(
            GeometryChecker.assert_continuous(self.reference, discountinuous_curve)
        )

        continuous_curve = CubicBezierCurve(
            Point(30, 30), Point(50, 10),
            Point(50, 30), Point(50, 30)
        )
        self.assertTrue(
            GeometryChecker.assert_continuous(self.reference, continuous_curve)
        )

    def test_2(self):
        """ Test assert_collinear """
        collinear = [
            Point(1, 1),
            Point(2, 5),
            Point(4, 13)
        ]
        self.assertTrue(
            GeometryChecker.assert_collinear(*collinear)
        )

        noncollinear = [
            Point(1, 1),
            Point(2, 5),
            Point(11, 43)
        ]
        self.assertFalse(
            GeometryChecker.assert_collinear(*noncollinear)
        )

    def test_3(self):
        """ Test assert_differentiable """
        nondifferentiable_curve = CubicBezierCurve(
            Point(30, 30), Point(50, 10),
            Point(50, 30), Point(50, 30)
        )
        self.assertFalse(
            GeometryChecker.assert_differentiable(self.reference, nondifferentiable_curve)
        )

        differentiable_curve = CubicBezierCurve(
            Point(30, 30), Point(10, 50),
            Point(30, 50), Point(30, 50)
        )
        self.assertTrue(
            GeometryChecker.assert_differentiable(self.reference, differentiable_curve)
        )


class TestSVGPathConverter(unittest.TestCase):
    """ SVGPathConverter tests """
    def test_1(self):
        """ Test Path to SVG string conversion """
        target_string = "M 10 30 C 10 10 30 10 30 30 C 30 50 30 50 10 50"
        curve1 = CubicBezierCurve(
            Point(10, 30), Point(30, 30),
            Point(10, 10), Point(30, 10)
        )
        curve2 = CubicBezierCurve(
            Point(30, 30), Point(10, 50),
            Point(30, 50), Point(30, 50)
        )
        path = Path([curve1, curve2])
        self.assertEqual(
            target_string,
            SVGPathConverter.path_to_string(path)
        )


if __name__ == '__main__':
    unittest.main()

import unittest
import vector_mandalas.bezier as bezier


class TestPoint(unittest.TestCase):
    """ Point tests """
    def test_1(self):
        """ Point creation """
        p = bezier.Point(10, 20)
        self.assertEqual(10, p.x)
        self.assertEqual(20, p.y)

    def test_2(self):
        """ Point Copying """
        p1 = bezier.Point(1, 2)
        p2 = p1.copy()
        self.assertIsNot(p1, p2)

        p3 = p1.copy(2, 2)
        self.assertEqual(3, p3.x)
        self.assertEqual(4, p3.y)


class TestCubicBezierCurve(unittest.TestCase):
    """ Cubic bezier curve tests """
    def setUp(self):
        self.start = bezier.Point(10, 10)
        self.end = bezier.Point(30, 10)
        self.cp1 = bezier.Point(10, 30)
        self.cp2 = bezier.Point(30, 30)

    def test_1(self):
        """ Line creation """
        linear_curve = bezier.CubicBezierCurve(self.start, self.end)

    def test_2(self):
        """ Quadratic curve creation """
        quadratic_curve = bezier.CubicBezierCurve(self.start, self.end, self.cp1, self.cp1)

    def test_3(self):
        """ Cubic curve creation """
        cubic_curve = bezier.CubicBezierCurve(self.start, self.end, self.cp1, self.cp2)


class TestPath(unittest.TestCase):
    """ Bezier Path tests """
    pass


class TestCurveChecker(unittest.TestCase):
    """ CurveChecker tests """
    def setUp(self):
        self.reference = bezier.CubicBezierCurve(
            bezier.Point(10, 30), bezier.Point(30, 30),
            bezier.Point(10, 10), bezier.Point(30, 10)
        )  # reference

    def test_1(self):
        """ Test assert_continuous """
        discountinuous_curve = bezier.CubicBezierCurve(
            bezier.Point(30, 40), bezier.Point(10, 60),
            bezier.Point(30, 60), bezier.Point(30, 60)
        )
        self.assertFalse(
            bezier.assert_continuous(self.reference, discountinuous_curve)
        )

        continuous_curve = bezier.CubicBezierCurve(
            bezier.Point(30, 30), bezier.Point(50, 10),
            bezier.Point(50, 30), bezier.Point(50, 30)
        )
        self.assertTrue(
            bezier.assert_continuous(self.reference, continuous_curve)
        )

    def test_2(self):
        """ Test assert_collinear """
        collinear = [
            bezier.Point(1, 1),
            bezier.Point(2, 5),
            bezier.Point(4, 13)
        ]
        self.assertTrue(
            bezier.assert_collinear(*collinear)
        )

        noncollinear = [
            bezier.Point(1, 1),
            bezier.Point(2, 5),
            bezier.Point(11, 43)
        ]
        self.assertFalse(
            bezier.assert_collinear(*noncollinear)
        )

    def test_3(self):
        """ Test assert_differentiable """
        nondifferentiable_curve = bezier.CubicBezierCurve(
            bezier.Point(30, 30), bezier.Point(50, 10),
            bezier.Point(50, 30), bezier.Point(50, 30)
        )
        self.assertFalse(
            bezier.assert_differentiable(self.reference, nondifferentiable_curve)
        )

        differentiable_curve = bezier.CubicBezierCurve(
            bezier.Point(30, 30), bezier.Point(10, 50),
            bezier.Point(30, 50), bezier.Point(30, 50)
        )
        self.assertTrue(
            bezier.assert_differentiable(self.reference, differentiable_curve)
        )


class TestSVGPathConverter(unittest.TestCase):
    """ SVGPathConverter tests """
    def test_1(self):
        """ Test Path to SVG string conversion """
        target_string = "M 10 30 C 10 10 30 10 30 30 C 30 50 30 50 10 50"
        curve1 = bezier.CubicBezierCurve(
            bezier.Point(10, 30), bezier.Point(30, 30),
            bezier.Point(10, 10), bezier.Point(30, 10)
        )
        curve2 = bezier.CubicBezierCurve(
            bezier.Point(30, 30), bezier.Point(10, 50),
            bezier.Point(30, 50), bezier.Point(30, 50)
        )
        path = bezier.Path([curve1, curve2])
        self.assertEqual(
            target_string,
            bezier.path_to_string(path)
        )


if __name__ == '__main__':
    unittest.main()

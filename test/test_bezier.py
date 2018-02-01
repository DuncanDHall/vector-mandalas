import unittest
import vector_mandalas.bezier as bezier


# class TestPoint(unittest.TestCase):
#     """ Point tests """
#     def test_1(self):
#         """ Point creation """
#         p = (10, 20)
#         self.assertEqual(10, p.x)
#         self.assertEqual(20, p.y)
#
#     def test_2(self):
#         """ Point Copying """
#         p1 = bezier.Point(1, 2)
#         p2 = p1.copy()
#         self.assertIsNot(p1, p2)


class TestCubicBezierCurve(unittest.TestCase):
    """ Cubic bezier curve tests """
    def setUp(self):
        self.start = (10, 10)
        self.end = (30, 10)
        self.cp1 = (10, 30)
        self.cp2 = (30, 30)

    def test_1(self):
        """ Line creation """
        linear_curve = bezier.CubicBezierCurve(self.start, self.end)
        self.assertIsNotNone(linear_curve.p1)
        self.assertIsNotNone(linear_curve.p2)
        self.assertIsNotNone(linear_curve.c1)
        self.assertIsNotNone(linear_curve.c2)

    def test_2(self):
        """ Quadratic curve creation """
        quadratic_curve = bezier.CubicBezierCurve(self.start, self.end, self.cp1, self.cp1)

    def test_3(self):
        """ Cubic curve creation """
        cubic_curve = bezier.CubicBezierCurve(self.start, self.end, self.cp1, self.cp2)


class TestPath(unittest.TestCase):
    """ Bezier Path tests """
    def test_1(self):
        """ Path initialization from_ints tests """
        path = bezier.Path.from_floats(
            10, 10,
            30, 10, 30, 10, 31, 30,
            30, 50, 50, 30, 50, 50
        )

        self.assertEqual(31, path[0].p2[0])


class TestCurveChecker(unittest.TestCase):
    """ CurveChecker tests """
    def setUp(self):
        self.reference = bezier.CubicBezierCurve(
            (10, 30), (30, 30),
            (10, 10), (30, 10)
        )  # reference

    def test_1(self):
        """ Test assert_continuous """
        discountinuous_curve = bezier.CubicBezierCurve(
            (30, 40), (10, 60),
            (30, 60), (30, 60)
        )
        self.assertFalse(
            bezier.assert_continuous(self.reference, discountinuous_curve)
        )

        continuous_curve = bezier.CubicBezierCurve(
            (30, 30), (50, 10),
            (50, 30), (50, 30)
        )
        self.assertTrue(
            bezier.assert_continuous(self.reference, continuous_curve)
        )

    def test_2(self):
        """ Test assert_collinear """
        collinear = [
            (1, 1),
            (2, 5),
            (4, 13)
        ]
        self.assertTrue(
            bezier.assert_collinear(*collinear)
        )

        noncollinear = [
            (1, 1),
            (2, 5),
            (11, 43)
        ]
        self.assertFalse(
            bezier.assert_collinear(*noncollinear)
        )

    def test_3(self):
        """ Test assert_differentiable """
        nondifferentiable_curve = bezier.CubicBezierCurve(
            (30, 30), (50, 10),
            (50, 30), (50, 30)
        )
        self.assertFalse(
            bezier.assert_differentiable(self.reference, nondifferentiable_curve)
        )

        differentiable_curve = bezier.CubicBezierCurve(
            (30, 30), (10, 50),
            (30, 50), (30, 50)
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
            (10, 30), (30, 30),
            (10, 10), (30, 10)
        )
        curve2 = bezier.CubicBezierCurve(
            (30, 30), (10, 50),
            (30, 50), (30, 50)
        )
        path = bezier.Path([curve1, curve2])
        self.assertEqual(
            target_string,
            bezier.path_to_string(path)
        )


if __name__ == '__main__':
    unittest.main()

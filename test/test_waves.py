import unittest

import svgwrite

from vector_mandalas import bezier
from vector_mandalas.bezier import CubicBezierCurve, Path, Point
from vector_mandalas import waves


class TestWaves(unittest.TestCase):
    def test_circle_gen(self):
        circle: Path = waves.gen_circle((100, 100), 50)
        circle_string = bezier.path_to_string(circle)

        dwg = svgwrite.Drawing('./drawings/test_circle.svg', size=(200, 200), profile='tiny')
        dwg.stroke(color=svgwrite.rgb(80, 100, 120), width=1)

        dwg.add(dwg.path(d=circle_string, fill="none"))

        dwg.save()

    def test_intermediate_point(self):
        p1: Point = (0.0, 0.0)
        p2: Point = (8.0, 6.0)

        mid: Point = waves.intermediate_point(p1, p2, 0.5)
        self.assertEqual((4.0, 3.0), mid)

        intermediate: Point = waves.intermediate_point(p1, p2, 0.25)
        self.assertEqual((2.0, 1.5), intermediate)

    def test_curve_split(self):
        curve = CubicBezierCurve(
            (50, 50), (150, 50),
            (75, 25), (125, 25),
        )
        two_curves = waves.split_curve(curve, [0.3])
        self.assertEqual(2, len(two_curves))
        three_curves = waves.split_curve(curve, [0.2, 0.6])
        self.assertEqual(3, len(three_curves))

        dwg = svgwrite.Drawing('./drawings/test_split.svg', size=(200, 200), profile='tiny')
        dwg.stroke(color=svgwrite.rgb(80, 100, 120), width=1)

        dwg.add(dwg.path(d=bezier.path_to_string(Path([curve])), fill="none"))
        dwg.add(dwg.path(d=bezier.path_to_string(Path(two_curves)), fill="none"))
        dwg.add(dwg.path(d=bezier.path_to_string(Path(three_curves)), fill="none"))

        dwg.save()


if __name__ == '__main__':
    unittest.main()

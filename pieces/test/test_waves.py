import unittest

from vector_mandalas import bezier
from vector_mandalas.bezier import CubicBezierCurve
from pieces.waves import waves

import svgwrite


class TestWaves(unittest.TestCase):
    def test_1(self):
        """ Circle generation """
        circle: bezier.Path = waves.gen_circle((100, 100), 50)
        circle_string = bezier.path_to_string(circle)
        print(circle_string)

        dwg = svgwrite.Drawing('pieces/test/drawings/test_circle.svg', size=(200, 200), profile='tiny')
        dwg.stroke(color=svgwrite.rgb(80, 100, 120), width=1)

        dwg.add(dwg.path(d=circle_string, fill="none"))

        dwg.save()

    def test_2(self):
        """ sanity check """
        curve = bezier.Path.from_floats(
            50, 100,
            50, 50, 150, 150, 150, 100
        )
        curve_string = bezier.path_to_string(curve)

        dwg = svgwrite.Drawing('pieces/test/drawings/test_curve.svg', size=(200, 200), profile='tiny')
        dwg.stroke(color=svgwrite.rgb(80, 100, 120), width=1)

        dwg.add(dwg.path(d=curve_string, fill="none"))

        dwg.save()

    def test_3(self):
        """ Curve splitting """
        curve = CubicBezierCurve(
            (50, 50), (150, 50),
            (75, 25), (125, 25),
        )
        two_curves = waves.split_curve(curve, [0.3])
        three_curves = waves.split_curve(curve, [0.2, 0.6])


if __name__ == '__main__':
    unittest.main()

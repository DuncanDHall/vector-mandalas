import unittest
# import sys
# sys.path.append('../')

from vector_mandalas import bezier
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
        curve = bezier.Path.from_ints(
            50, 100,
            50, 50, 150, 150, 150, 100
        )
        curve_string = bezier.path_to_string(curve)

        dwg = svgwrite.Drawing('pieces/test/drawings/test_curve.svg', size=(200, 200), profile='tiny')
        dwg.stroke(color=svgwrite.rgb(80, 100, 120), width=1)

        dwg.add(dwg.path(d=curve_string, fill="none"))

        dwg.save()


if __name__ == '__main__':
    unittest.main()
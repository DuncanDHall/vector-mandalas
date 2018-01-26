""" This file contains test code for the svgwrite library """

import svgwrite

dwg = svgwrite.Drawing('test_curve.svg', size=(200, 200), profile='tiny')  # TODO: what is a profile??

dwg.add(dwg.line((10, 10), (30, 30)))
dwg.add(dwg.line((20, 10), (40, 30)))

# define default stroke for all paths
dwg.stroke(color=svgwrite.rgb(80, 100, 120), width=1)

# This defines a triangle. More info here: https://www.w3.org/TR/SVG11/paths.html#PathData
dwg.add(dwg.path(d="M 100 100 L 300 100 L 200 300 z"))

# This defines a curve
my_curve = dwg.path(d="M 50 10 c 20 20 100 20 0 50", fill="none")
dwg.add(my_curve)

dwg.save()

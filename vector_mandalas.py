import svgwrite

from vector_mandalas import bezier


if __name__ == "__main__":

    linear_path = bezier.Path([
        bezier.CubicBezierCurve(
            (20, 20), (180, 180)
        )
    ])

    cubic_path = bezier.Path.from_floats([
        20, 20,
        10, 100, 10, 100, 100, 100,
        180, 100, 180, 100, 180, 180
    ])

    dwg = svgwrite.Drawing('testing.svg', size=(200, 200), profile='tiny')

    dwg.stroke(color=svgwrite.rgb(80, 100, 120), width=1)

    dwg.add(dwg.path(d=bezier.path_to_string(linear_path)))
    dwg.add(dwg.path(d=bezier.path_to_string(cubic_path)))

    dwg.save()

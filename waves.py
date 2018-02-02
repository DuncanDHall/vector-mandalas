import numpy as np
import svgwrite
import os

from vector_mandalas import bezier, waves_helper
from vector_mandalas.bezier import Path, Point


##############################
# Global Config              #
##############################

CANVAS_SIZE = (1000, 1000)
DIAMETER_RATIO = 0.8
SPLITS_PER_QUAD = 6

LINE_COLOR = svgwrite.rgb(80, 100, 120)

FILE_Name = "base.svg"


def main() -> None:

    # collect paths for each layer here
    layers = []

    ##############################
    # Base Circle                #
    ##############################

    plain_circle: Path = waves_helper.gen_circle(
        (CANVAS_SIZE[0] / 2, CANVAS_SIZE[1] / 2),
        DIAMETER_RATIO * CANVAS_SIZE[0] / 2
    )

    quarter_splits = list(np.linspace(0.0, 1.0, SPLITS_PER_QUAD, endpoint=False)[1:])
    base_curves = []

    for i, curve in enumerate(plain_circle):
        base_curves += waves_helper.split_curve(curve, quarter_splits)

    layers.append(Path(base_curves))

    ##############################
    # Control Variations         #
    ##############################



    ##############################
    # Final Drawing              #
    ##############################

    dwg = svgwrite.Drawing(
        os.path.join('./drawings/', FILE_Name),
        size=CANVAS_SIZE, profile='tiny'
    )
    dwg.stroke(color=LINE_COLOR, width=1)
    for path in layers:
        dwg.add(dwg.path(d=bezier.path_to_string(path), fill="none"))
    dwg.save()


if __name__ == "__main__":
    main()
    print("done")

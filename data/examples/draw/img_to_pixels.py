import numpy as np
import taichi as ti

from tolvera import Tolvera, run
from tolvera.pixels import Pixels


def main(**kwargs):
    tv = Tolvera(x=1680, y=1050, **kwargs)

    path = "/home/kanak/Desktop/GSOC/Python/tolvera/tolvera-examples/images/multi_color.jpg"

    img_px = Pixels(tv)
    img_px.from_img(path)
    tv.px.set(img_px)  # alternative to blending
    # tv.px.blur(10)

    @tv.render
    def _():
        # tv.px.diffuse(0.99)
        # tv.px.blend_mix(img_px, 0.5)
        return tv.px


if __name__ == "__main__":
    run(main)

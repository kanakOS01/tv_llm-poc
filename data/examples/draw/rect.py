"""Draw a rectangle in the center of the screen."""

import taichi as ti

from tolvera_poc import Tolvera, run


def main(**kwargs):
    tv = Tolvera(**kwargs)

    @ti.kernel
    def draw():
        w = 100
        tv.px.rect(
            tv.x / 2 - w / 2, tv.y / 2 - w / 2, w, w, ti.Vector([1.0, 0.0, 0.0, 1.0])
        )

    @tv.render
    def _():
        draw()
        return tv.px


if __name__ == "__main__":
    run(main)

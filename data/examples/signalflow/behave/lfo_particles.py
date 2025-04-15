"""
Modulate particle movement with an LFO.
"""

import taichi as ti
from signalflow import *

from tolvera_poc import Tolvera, run


def main(**kwargs):
    tv = Tolvera(**kwargs)

    graph = AudioGraph()
    lfo = SineLFO(0.5, 0, 10)
    lfo.play()

    @tv.render
    def _():
        tv.px.diffuse(0.99)
        tv.v.move(tv.p, lfo.output_buffer[0][0])
        tv.px.particles(tv.p, tv.s.species())
        return tv.px


if __name__ == "__main__":
    run(main)

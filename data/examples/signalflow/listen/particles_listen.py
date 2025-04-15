import numpy as np
import taichi as ti
from signalflow import *

from tolvera_poc import Tolvera, run
from tolvera.osc.update import Updater
from tolvera.utils import map_range


class Sine(Patch):
    def __init__(self, freq=880, gain=1.0, pan=0.0):
        super().__init__()
        freq = self.add_input("freq", freq)
        gain = self.add_input("gain", gain)
        pan = self.add_input("pan", pan)
        sine = SineOscillator(freq)
        panner = StereoPanner(sine, pan)
        output = panner * gain
        self.set_output(output)
        self.set_auto_free(True)

    def __setattr__(self, name, value):
        self.set_input(name, value)


def main(**kwargs):
    tv = Tolvera(**kwargs)

    config = AudioGraphConfig()
    config.output_buffer_size = kwargs.get("output_buffer_size", 8192)
    graph = AudioGraph(config)

    num_sines = tv.pn
    freq, pan, gain = (100, 10000), (-1, 1), (0, 1 / num_sines)
    freqs = [np.random.uniform(*freq) for _ in range(num_sines)]
    pans = [np.random.uniform(*pan) for _ in range(num_sines)]
    gains = [np.random.uniform(*gain) for _ in range(num_sines)]
    sines = [Sine(freq, gain, pan) for freq, gain, pan in zip(freqs, gains, pans)]

    tv.s.oscs_p = {
        "state": {
            "freq": (ti.f32, 100.0, 10000.0),
            "pan": (ti.f32, -1.0, 1.0),
            "gain": (ti.f32, 0.0, 1.0),
        },
        "shape": num_sines,
        "randomise": True,
    }

    @ti.kernel
    def listen():
        pass

    def _update():
        nonlocal freq, pan, gain, freqs, pans, gains
        p_np = tv.p.field.to_numpy()
        pos = p_np["pos"]
        mag = np.sqrt(np.sum(p_np["vel"] ** 2, axis=1))
        pans = map_range(pos.T[0], 0, tv.x, *pan)
        freqs = map_range(pos.T[0], 0, tv.x, *freq)
        gains = map_range(mag, 0, 1, *gain)
        for i, s in enumerate(sines):
            s.pan = pans[i]
            s.freq = freqs[i]
            s.gain = gains[i]

    _update()
    updater = Updater(_update, 1)

    def play():
        [s.play() for s in sines]

    def stop():
        [s.stop() for s in sines]

    play()

    @tv.cleanup
    def _():
        stop()

    @tv.render
    def _():
        updater()
        tv.px.diffuse(0.99)
        # tv.v.attract(tv.p, [tv.x/2, tv.y/2], 1, tv.x)
        tv.v.flock(tv.p)
        tv.px.particles(tv.p, tv.s.species())
        return tv.px


if __name__ == "__main__":
    run(main)

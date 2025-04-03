"""Mapping particle positions to RAVE latent space via IML.

RAVE: https://github.com/acids-ircam/RAVE
Models: https://huggingface.co/Intelligent-Instruments-Lab/rave-models

Example:
    $ python iml_mp_to_rave.py --iml True --audio_device [4,5] --rave_path /path/to/rave_model.ts --cv True --camera True --device 1 --pose True
"""

import numpy as np
import sounddevice as sd
import torch
from iipyper import Audio

from tolvera import Tolvera, run
from tolvera.utils import map_range


def main(**kwargs):
    print(f"Availabe audio devices:\n{sd.query_devices()}")

    tv = Tolvera(**kwargs)
    rave_path = kwargs.get("rave_path", None)
    device = kwargs.get("audio_device", None)
    assert rave_path is not None, "RAVE model path required."
    assert (
        device is not None
    ), f"Audio device required. Availabe devices:\n{sd.query_devices()}"

    rave = torch.jit.load(rave_path)

    try:
        sr = rave.sr
    except Exception:
        sr = rave.sampling_rate

    z = torch.zeros(rave.encode_params[2])

    def rave_callback(
        indata: np.ndarray, outdata: np.ndarray, frames: int, time, status
    ):
        with torch.inference_mode():
            outdata[:, :] = rave.decode(z[None, :, None])[:, 0].T

    audio = Audio(
        device=device,
        dtype=np.float32,
        samplerate=sr,
        blocksize=rave.encode_params[-1],
        callback=rave_callback,
    )

    tv.iml.mp_pose2rave = {
        "type": "fun2vec",
        "size": (tv.s.pose.size, rave.encode_params[2]),
        "io": (tv.s.pose.to_vec, None),
        "randomise": True,
        # 'rand_method': 'uniform',
        # 'rand_kw': {'low': -3, 'high': 3},
        # 'config': {'interpolate': 'Ripple'},
        # 'default_kwargs': {'k': 10, 'ripple_depth': 5, 'ripple': 5}
    }

    def update():
        nonlocal z
        outvec = tv.iml.o["mp_pose2rave"]
        if outvec is not None:
            # print('outvec',outvec)
            z[:] = torch.from_numpy(outvec)

    audio.stream.start()

    @tv.render
    def _():
        update()
        tv.cv()
        # tv.cv.px.flip_y()
        # tv.v.flock(tv.p)
        tv.px.clear()
        # tv.px.diffuse(0.99)
        # tv.pose(np.flip(tv.cv.cc_frame, axis=1))
        tv.pose(tv.cv.cc_frame)
        tv.pose.draw()
        # if tv.pose.detected[None] == 1:
        #     attract()
        tv.px.particles(tv.p, tv.s.species())
        return tv.px


if __name__ == "__main__":
    run(main)

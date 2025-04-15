"""Interactive machine learning example

Using the flock model, we map its particle states to its species rules,
creating a feedback loop between them.

The IML 'type' is 'fun2fun' because we are mapping a function to another function.

Example
  $ python iml_flock_particles_to_species.py --iml True
"""

from tolvera_poc import Tolvera, run


def main(**kwargs):
    tv = Tolvera(**kwargs)

    """/anguilla/add "input" ... "output" ... "instance" <name>"""
    """/anguilla/add "input" ... "output" ... "instance" flock_p2flock_s"""
    tv.iml.flock_p2flock_s = {
        "size": (tv.s.flock_p.size, tv.s.flock_s.size),
        "io": (tv.s.flock_p.to_vec, tv.s.flock_s.from_vec),
        "randomise": True,
    }

    # tv.iml.flock_p2flock_s.save('file.json')

    @tv.render
    def _():
        tv.px.diffuse(0.99)
        tv.v.flock(tv.p)
        tv.px.particles(tv.p, tv.s.species)
        return tv.px


if __name__ == "__main__":
    run(main)

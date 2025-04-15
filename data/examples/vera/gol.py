import taichi as ti

from tolvera_poc import Tolvera, run


def main(**kwargs):
    tv = Tolvera(x=1000, y=1000, gol_alive_c=[0.8, 0.8, 0.3, 0.5])

    # tv.v.gol.set_speed(10)

    def draw(s: ti.template()):
        tv.px.stamp(0, 0, s)

    @tv.render
    def _():
        return tv.v.gol()

    # # Alternatively:
    # @tv.render
    # def _():
    #     tv.px.clear()
    #     s = tv.v.gol()
    #     draw(s)
    #     return tv.px


if __name__ == "__main__":
    run(main)

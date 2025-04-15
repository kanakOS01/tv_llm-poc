import taichi as ti
from tolvera import Tolvera, run

def main(**kwargs):
    tv = Tolvera(**kwargs)

    @ti.kernel
    def draw():
        w = 50  # Width and height of the rectangles
        colors = [
            ti.Vector([1.0, 0.0, 0.0, 1.0]),  # Red
            ti.Vector([0.0, 1.0, 0.0, 1.0]),  # Green
            ti.Vector([0.0, 0.0, 1.0, 1.0]),  # Blue
            ti.Vector([1.0, 1.0, 0.0, 1.0]),  # Yellow
        ]
        
        # Draw each rectangle centered on the screen
        for i in range(4):
            x_offset = (i % 2) * (w + 10) - 10  # Horizontal offset
            y_offset = (i // 2) * (w + 10) - 10  # Vertical offset
            tv.px.rect(tv.x / 2 + x_offset, tv.y / 2 + y_offset, w, w, colors[i])

    @tv.render
    def _():
        tv.p()
        draw()
        return tv.px

if __name__ == '__main__':
    run(main)
import sys
import math
import matplotlib.pyplot as plt


DEEP_LEVEL = 5

POINT_A = (-1.5, 0.0)
POINT_B = (1.5, 0.0)
POINT_C = (0, 2.598076211)


def split_segment_with_triangle(points):
    point_a, point_b = points
    x1, y1 = point_a
    x2, y2 = point_b

    vx = x2 - x1
    vy = y2 - y1
    length = math.hypot(vx, vy)

    s = length / 3.0
    h = (math.sqrt(3) / 2.0) * s

    ux = vx / length
    uy = vy / length

    mx = (x1 + x2) / 2.0
    my = (y1 + y2) / 2.0

    half_base = s / 2.0

    bx = mx - ux * half_base
    by = my - uy * half_base
    cx = mx + ux * half_base
    cy = my + uy * half_base

    nx = -uy
    ny = ux

    tx = mx + nx * h
    ty = my + ny * h

    segments = [
        ((x1, y1), (bx, by)),
        ((bx, by), (tx, ty)),
        ((tx, ty), (cx, cy)),
        ((cx, cy), (x2, y2)),
    ]

    return segments


def draw_fractal(ax, points, level):
    if level == 0:
        point_A, point_B = points
        x1, y1 = point_A
        x2, y2 = point_B
        ax.plot([x1, x2], [y1, y2], color="blue", linewidth=3)
        return

    segments = split_segment_with_triangle(points)
    for s in segments:
        draw_fractal(ax, s, level - 1)


def main():
    if len(sys.argv) < 2:
        deep_level = DEEP_LEVEL
        
    else:
        arg = sys.argv[1]
        try:
            deep_level = int(arg)
        except ValueError:
            print("Error: argument must be an integer number")
            return

        if deep_level <= 0:
            print("Error: number must be positive")
            return

    fig, ax = plt.subplots()
    draw_fractal(ax, (POINT_A, POINT_C), deep_level)
    draw_fractal(ax, (POINT_C, POINT_B), deep_level)
    draw_fractal(ax, (POINT_B, POINT_A), deep_level)

    ax.set_aspect("equal")
    ax.set_axis_off()
    plt.show()


if __name__ == "__main__":
    main()

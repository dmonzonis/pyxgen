#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
import argparse
from random import choice
from copy import deepcopy
from PIL import Image


def count_neighbors(state, x, y):
    """
    Count live cells next to the given position on the x and
    y axis.
    """
    count = 0
    if x > 0:
        count += state[y][x - 1] == 1
    if y > 0:
        count += state[y - 1][x] == 1
    if x < len(state[y]) - 1:
        count += state[y][x + 1] == 1
    if y < len(state) - 1:
        count += state[y + 1][x] == 1
    return count


def evolve(state):
    """
    Cellular automata algorithm to change the state of a bitmap according to the
    following rules:
        - Any live cell with two or three neighbors survives.
        - Any dead cell with one or less live neighbors becomes a live cell.
        - All other live cells die in the next generation. Similarly, all other dead
        cells stay dead.
    """
    new_state = deepcopy(state)
    for y in range(len(state)):
        for x, cell in enumerate(state[y]):
            neighbors = count_neighbors(state, x, y)
            new_state[y][x] = int((cell == 0 and neighbors <= 1) or (
                cell == 1 and (neighbors == 2 or neighbors == 3)))
    return new_state


def generate_bitmap():
    """
    Creates a 10x10 bitmap representing the sprite image.
    The bitmap is a matrix with codes 0, 1 or 2.
    0 means background, 1 normal color and 2 outline color.
    """
    # Create 4x8 white noise
    bitmap = [[choice([0, 1]) for _ in range(4)] for _ in range(8)]
    # Evolve 2 times
    bitmap = evolve(evolve(bitmap))

    # To add the outline, the image will grow in 2 pixels in each direction except the mirror
    for line in bitmap:
        line.insert(0, 0)
    bitmap.insert(0, [0] * len(bitmap[0]))
    bitmap.append([0] * len(bitmap[0]))

    for y in range(len(bitmap)):
        for x, cell in enumerate(bitmap[y]):
            if cell == 0 and count_neighbors(bitmap, x, y) > 0:
                bitmap[y][x] = 2  # mark as outline

    return bitmap


def create_sprite(bitmap, color=(0, 255, 0), outline_color=(0, 185, 0),
                  bg_color=(255, 255, 255), transparency=False):
    """
    Processes the 10x10 bitmap and returns the image produced by interpreting the codes with
    the given colors.
    """
    # Mirror image
    for line in bitmap:
        line.extend(line[::-1])

    # Create image
    img = Image.new('RGBA', (10, 10))
    color_map = {
        0: bg_color if not transparency else (255, 255, 255, 0),
        1: color,
        2: outline_color
    }
    for y in range(len(bitmap)):
        for x, cell in enumerate(bitmap[y]):
            img.putpixel((x, y), color_map[cell])
    return img


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--color', '-c', type=int, nargs=3, help="Main color of the sprite",
                        default=(0, 255, 0))
    parser.add_argument('--outline', '-o', type=int, nargs=3, help="Color of the sprite's outline",
                        default=(0, 185, 0))
    parser.add_argument('--background', '-b', type=int, nargs=3, help="Color of the background",
                        default=(255, 255, 255))
    parser.add_argument('--transparency', '-t', action='store_true',
                        help="Use transparent background")

    args = parser.parse_args()

    img = create_sprite(generate_bitmap(), tuple(args.color),
                        tuple(args.outline), tuple(args.background),
                        args.transparency)
    # Save image to a file as PNG with a random filename
    random_filename = ''.join(choice(string.ascii_letters) for _ in range(16))
    img.save(random_filename + '.png')


if __name__ == "__main__":
    main()

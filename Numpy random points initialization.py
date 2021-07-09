import random

import numpy as np
from PIL import Image

IMAGE_WIDTH, IMAGE_HEIGHT = 200, 200
RANDOM_DOTS = 50  # Initial amount of dots to start with
COLOR_RANGE = -10, 10  # Number which will be added/subtracted from pixel values
PIXELS_AROUND = [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1]]
GENERATIONS_COUNT = 10  # Amount of times new pixels will be generated around existing ones

word_seed = 'Sososas'
binary_seed = word_seed.encode('utf-8')
int_seed = int.from_bytes(binary_seed, 'big')
random.seed(int_seed)


def create_empty_image():
    """Populate an empty array"""
    t = (IMAGE_WIDTH, IMAGE_HEIGHT, 3)
    arr = np.zeros(t, dtype=np.uint8)
    return arr


def populate_image_with_random_dots(image_arr, dots_number):
    """For rach dot in dots_number will be created a colored pixel"""
    for x in range(dots_number):
        i = random.randint(0, IMAGE_WIDTH - 1)
        j = random.randint(0, IMAGE_HEIGHT - 1)
        image_arr[i][j] = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
    return image_arr


def find_colored_pixels(image_arr):
    """Find all colored pixels and save them to an array"""
    colored_pixels = []
    two_dimentions = image_arr[:, :, 0]
    for i, col in enumerate(two_dimentions):
        for j, row in enumerate(col):
            if two_dimentions[i][j] != 0:
                colored_pixels.append((j, i))
    return colored_pixels


def draw_pixels_around(colored_pixels, im):
    """Draw pixels in a random direction from the existing ones"""
    for i in range(len(colored_pixels)):
        r_offset = random.randrange(COLOR_RANGE[0], COLOR_RANGE[1])
        g_offset = random.randrange(COLOR_RANGE[0], COLOR_RANGE[1])
        b_offset = random.randrange(COLOR_RANGE[0], COLOR_RANGE[1])

        next_pixel = random.choice(PIXELS_AROUND)

        x = colored_pixels[i][0]
        y = colored_pixels[i][1]
        x_offset = x + next_pixel[0]
        y_offset = y + next_pixel[1]
        pixel = im.getpixel((x, y))

        try:
            is_colored = im.getpixel((x_offset, y_offset))
            if is_colored[0] == 0 and is_colored[1] == 0 and is_colored[2] == 0:
                im.putpixel((x_offset, y_offset), (pixel[0] + r_offset, pixel[1] + g_offset, pixel[2] + b_offset))
                image_arr[y_offset][x_offset] = (pixel[0] + r_offset, pixel[1] + g_offset, pixel[2] + b_offset)
        except IndexError:
            pass


if __name__ == '__main__':
    image_arr = create_empty_image()
    image_arr = populate_image_with_random_dots(image_arr, RANDOM_DOTS)
    im = Image.fromarray(image_arr, "RGB")

    for i in range(GENERATIONS_COUNT):
        colored_pixels = find_colored_pixels(image_arr)
        draw_pixels_around(colored_pixels, im)

    # im.save('image.png')
    im.show()
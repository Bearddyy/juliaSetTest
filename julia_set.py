# Julia set implimentation

import numpy as np
import cv2
import tqdm
import random

def julia_set(c, n, x_min, x_max, y_min, y_max, width, height):
    """Create a julia set image

    Args:
        c (complex): Complex number
        n (int): Number of iterations
        x_min (float): Minimum x value
        x_max (float): Maximum x value
        y_min (float): Minimum y value
        y_max (float): Maximum y value
        width (int): Width of image
        height (int): Height of image

    Returns:
        numpy.ndarray: Julia set image
    """
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    z = x + y[:, None] * 1j
    image = np.zeros((height, width))
    for k in tqdm.tqdm(range(n)):
        z = z**2 + c
        mask = (np.abs(z) > 2) & (image == 0)
        image[mask] = k
        z[mask] = np.nan
    return -image.T

def main():
    """Main function
    """
    c = complex(-0.1, 0.65)
    n = 200
    x_min = -0.05
    x_max = 0.5
    y_min = -0.5
    y_max = 0.05
    width = 1000
    height = 1000
    while True:
        np_set = julia_set(c, n, x_min, x_max, y_min, y_max, width, height)
        # set returned is from -n to 0, so we need to convert to 0 to 255
        image = np.uint8(-np_set / n * 255)
        cv2.imshow('image', image)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        print('c = {}'.format(c))
        c = complex(random.uniform(-0.1, 0.1), 0.65)
if __name__ == '__main__':
    main()

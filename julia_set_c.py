# Utalise the c implimentation of the julia set

from ctypes import *
import numpy as np
from PIL import Image
import time
from functools import wraps

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

# Load the shared library
lib = cdll.LoadLibrary('./julia_set.so')

# Define the function return types
lib.julia_set.restype = None
lib.julia_set.argtypes = [
    c_uint32, # Width
    c_uint32, # Height
    c_uint32, # Iterations
    c_float, # Minimum x value
    c_float, # Maximum x value
    c_float, # Minimum y value
    c_float, # Maximum y value
    c_float, # c real part
    c_float, # c imaginary part
    POINTER(c_uint16) #image
]

# Call the function
@timeit
def julia_set_wrapper(c, n, x_min, x_max, y_min, y_max, width, height):
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
    image = np.zeros((height, width), dtype=np.uint16)
    
    lib.julia_set(
        width,
        height,
        n,
        x_min,
        x_max,
        y_min,
        y_max,
        c.real,
        c.imag,
        image.ctypes.data_as(POINTER(c_uint16))
    )
    return image

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
        
    np_set = julia_set_wrapper(c, n, x_min, x_max, y_min, y_max, width, height)

    # Set is returned as 16 bit, convert to 8 bit
    np_set = np_set / np.max(np_set) * 255
    
    # Write the image to disk
    image = Image.fromarray(np_set)
    image = image.convert('L')
    image.save('julia_set_c.png')

if __name__ == '__main__':
    main()
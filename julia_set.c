// Julia set implented in c

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <complex.h>

extern void julia_set(
    uint32_t width, // Width of the image
    uint32_t height, // Height of the image
    uint16_t max_iter, // Maximum number of iterations
    float x_min, // Minimum x value
    float x_max, // Maximum x value
    float y_min, // Minimum y value
    float y_max, // Maximum y value
    float c_real, // Real part of the complex constant
    float c_imag, // Imaginary part of the complex constant
    uint16_t *image // Output image
)
{
    // Create a complex number from the real and imaginary parts
    const double complex c = c_real + c_imag * I;

    // Calculate the step size in the x and y directions
    const double dx = (x_max - x_min) / (double)width;
    const double dy = (y_max - y_min) / (double)height;
    
    const double escape_radius_sq = 9.0; // (3.0 squared)

    for (uint32_t y = 0; y < height; y++) {
        for (uint32_t x = 0; x < width; x++) {
            // Map the pixel coordinates to the complex plane
            double real = x_min + x * dx;
            double imag = y_min + y * dy;
            double complex z = real + imag * I; // Create a complex number from real and imag

            uint16_t iter;
            for (iter = 0; iter < max_iter; iter++) {
                z = z * z + c; // Julia set iteration formula

                // Check if the point escapes to infinity
                if (cabs(z) > escape_radius_sq) {
                    break;
                }
            }

            image[y * width + x] = iter;
        }
    }
}
import matplotlib.pyplot as plt
import matplotlib.image as img
import pandas as pd

import numpy as np
from pycuda import driver, compiler, gpuarray, tools

# -- initialize the device
import pycuda.autoinit



kernel_code_template = """
__global__ void rgb2gray(unsigned int *grayimage, unsigned int *rgbimage)
{
    int x = threadIdx.x +  blockIdx.x * blockDim.x;
    int y = threadIdx.y + blockIdx.y * blockDim.y;

    if(x<%(width)s &&  y <%(height)s){

        int offsetgray = y * %(width)s + x;
        int rgboffset = offsetgray * 3;

        unsigned int r = rgbimage[rgboffset ];

        unsigned int g = rgbimage[rgboffset + 2];

        unsigned int b = rgbimage[rgboffset + 3];

        grayimage[offsetgray] = 0.21f*r +0.71f*g +0.07f*b;

    }
}
"""


image=img.imread("shingeki.jpg")
a= image.shape
print(a)


width= a[1]
height=a[0]

a_cpu = np.array(image).astype(np.uint8)
b_cpu = np.zeros((height, width,3 )).astype(np.uint8)

a_gpu = gpuarray.to_gpu(a_cpu) 
b_gpu = gpuarray.to_gpu(b_cpu)



print(width)
print(height)

kernel_code = kernel_code_template % {
    'width': width, 
    'height': height
    }


mod = compiler.SourceModule(kernel_code)

matrixmul = mod.get_function("rgb2gray")

matrixmul(
    # inputs
    b_gpu,  
    # output
    a_gpu,
    # (only one) block of MATRIX_SIZE x MATRIX_SIZE threads
    block = (6,36, 1),
    grid = (100,8,1),

    ) 






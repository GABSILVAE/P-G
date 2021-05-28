import numpy as np
from pycuda import driver, compiler, gpuarray, tools
import pycuda.autoinit
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import pandas as pd
import os

kernel_code_template = """
__global__ void rgb2gray(unsigned int *grayImage, unsigned int *rgbImage)
{
    int x = threadIdx.x + blockIdx.x * blockDim.x;

    int y = threadIdx.y + blockIdx.y * blockDim.y;

    if(x<%(width)s && y >%(height)s){

        int grayoffset = y * %(width)s + x;
        /* int rgboffset =grayoffset * 3;

        unsigned int r= rgbImage[rgboffset ];
        unsigned int g= rgbImage[rgboffset + 2]; 
        unsigned int b= rgbImage[rgboffset + 3];
        */

        grayImage[grayoffset]= rgbImage[grayoffset]; 
    } 

}

"""


BASE_DIR = os.getcwd()
print(BASE_DIR)
image=img.imread("shingeki.jpg")

a=image.shape
height =a[0]
width =a[1]

a_cpu = np.array(image).astype(np.uint8)
b_cpu = np.zeros((height, height)).astype(np.uint8)

a_gpu = gpuarray.to_gpu(a_cpu) 
b_gpu = gpuarray.to_gpu(b_cpu)




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

print(a)
#figure, axes = plt.subplots(2, 3)


'''axes[0, 1].imshow(a_gpu.get())
plt.show()

axes[0, 0].imshow(a_gpu.get())
plt.show()
'''
c= b_gpu.get()
print(c)


plt.imshow(c)
plt.show()
import numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt

from pycuda import compiler, gpuarray, tools
import pycuda.driver as cuda

# -- initialize the device
import pycuda.autoinit

import os

from PIL import Image


kernel_code_template = """
__global__ void MatrixMulKernel(float *rgbimage, float *grayimage, float *binimage)
{
    int tx = threadIdx.x + blockDim.x * blockIdx.x;
    int ty = threadIdx.y + blockDim.y * blockIdx.y;
     
    
    if(tx<%(columna)s && ty< %(fila)s){

        int grayOffset = %(columna)s * ty + tx;

        int rgbOffset = grayOffset * %(channels)s;

        unsigned int r = rgbimage[rgbOffset];

        unsigned int g = rgbimage[rgbOffset +1];

        unsigned int b = rgbimage[rgbOffset +2];

        grayimage[grayOffset] = ((r + g + b)/3);

        if(grayimage[grayOffset]<%(umbral)s){

            binimage[grayOffset]=0;
        }

        else{

            binimage[grayOffset]=1;
        }
    }
  


}
"""



image=img.imread("shingeki.jpg")
print(image.shape)
r_img= image[:,:,0]


fila,columna,canales = image.shape
image_array_list=[]

for row in range(fila):
    for column in range(columna):
        for channel in range (canales):
            image_array_list.append(image[row][column][channel])

image_list=np.array(image_array_list)

print(image_list.shape)

image_rgb= np.array(image_list). astype(np.float32)
image_gray=np.zeros((fila,columna)). astype(np.float32)
image_bin=np.zeros((fila,columna)). astype(np.float32)


rgb_gpu = cuda.mem_alloc(image_rgb.nbytes)
gray_gpu = cuda.mem_alloc(image_gray.nbytes)
bin_gpu = cuda.mem_alloc(image_bin.nbytes)

umbral=150

kernel_code = kernel_code_template % {
    'fila': fila, 
    'columna': columna,
    'channels':canales,
    'umbral': umbral
    }

mod = compiler.SourceModule(kernel_code)

matrixmul = mod.get_function("MatrixMulKernel")


cuda.memcpy_htod(rgb_gpu, image_rgb)

matrixmul(
    # inputs
    rgb_gpu,  
    #output
    gray_gpu,
    bin_gpu,
    # (only one) block of MATRIX_SIZE x MATRIX_SIZE threads
    block = (6,36, 1),
    grid = (100,8,1),

    ) 

gr= np.zeros((fila, columna)). astype(np.float32)
bn= np.zeros((fila, columna)). astype(np.float32)


cuda.memcpy_dtoh(gr, gray_gpu)

cuda.memcpy_dtoh(bn, bin_gpu)
bn= bn.astype(np.uint8)

print(kernel_code)
print(bn.shape)

image = Image.fromarray(bn).save('pic1.png')
'''umbral = image.convert("L")

base_dir = os.getcwd()
folder_images = 'images'
path = os.path.join(base_dir, folder_images)
if not (os.path.exists(path)):
    os.mkdir(path)
image_path = os.path.join(path,'umbral.jpeg')
#umbral.save(image_path)
'''


#figure, axes = plt.subplots(1)
plt.imshow(bn,cmap='gray')
#axes[1].imshow(gr,cmap='gray')
#axes[2].imshow(bn,cmap='gray')
plt.savefig("binarizada.jpeg")
plt.show()

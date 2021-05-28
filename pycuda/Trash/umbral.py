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
__global__ void MatrixMulKernel( float *grayimage, float *binimage)
{
    int tx = threadIdx.x + blockDim.x * blockIdx.x;
    int ty = threadIdx.y + blockDim.y * blockIdx.y;
     
    
    if(tx<%(columna)s && ty< %(fila)s){

       
        int offsetgray = ty * %(columna)s + tx;

        if(grayimage[offsetgray]<%(umbral)s){

            binimage[offsetgray]=0;
        }

        else{

            binimage[offsetgray]=1;
        }
    }
  


}
"""



image=img.imread("shingeki_gray.jpeg")
print(image.shape)
r_img= image[:,:,0]


fila,columna = r_img.shape



image_list=np.array(r_img)

print(image_list.shape)

image_rgb= np.array(image_list). astype(np.float32)

image_bin=np.zeros((fila,columna)). astype(np.float32)


r_gpu = cuda.mem_alloc(image_rgb.nbytes)

bin_gpu = cuda.mem_alloc(image_bin.nbytes)

umbral=150

kernel_code = kernel_code_template % {
    'fila': fila, 
    'columna': columna,
    'umbral': umbral
    }

mod = compiler.SourceModule(kernel_code)

matrixmul = mod.get_function("MatrixMulKernel")


cuda.memcpy_htod(r_gpu, image_rgb)

matrixmul(
    # inputs
    r_gpu,  
    #output
    bin_gpu,
    # (only one) block of MATRIX_SIZE x MATRIX_SIZE threads
    block = (6,36, 1),
    grid = (100,8,1),

    ) 

gr= np.zeros((fila, columna)). astype(np.float32)
bn= np.zeros((fila, columna)). astype(np.float32)



cuda.memcpy_dtoh(bn, bin_gpu)
bn= bn.astype(np.uint8)

print(kernel_code)
print(bn.shape)

#image = Image.fromarray(bn).save('pic1.png')
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

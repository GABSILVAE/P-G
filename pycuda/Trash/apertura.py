#erosión y depues dilatación 

import numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt
from numpy.core.records import array

from pycuda import compiler, gpuarray, tools
import pycuda.driver as cuda

# -- initialize the device
import pycuda.autoinit

kernel_code_template_erosion = """
__global__ void erosion(unsigned int *image, unsigned int *kernel, unsigned int *imagefiltred)
{
    int tx = threadIdx.x + blockDim.x * blockIdx.x;
    int ty = threadIdx.y + blockDim.y * blockIdx.y;
   
    int kernelRowRadius = (%(filfiltro)s-1)/2;
    int kernelColRadius = (%(columnfiltro)s-1)/2;

    if(ty<%(fila)s && tx<%(columna)s){
        int startRow= ty - kernelRowRadius;
        int startColumn= tx - kernelColRadius;
        int a=0;
        for (int i=0; i<%(filfiltro)s; i++){
            for (int j=0; j<%(columnfiltro)s; j++){
                int currentRow = startRow + i;
                int currentCol = startColumn + j;
                if(currentRow>=0 && currentRow<%(fila)s && currentCol>=0 && currentCol<%(columna)s){                  
                    if(kernel[i * %(filfiltro)s +j]==1 && image[currentRow * %(columna)s + currentCol]==0){
                        a=1;
                        imagefiltred[ty * %(columna)s + tx] = 0;
                    }
                    else{
                        if(a!=1 && i==(%(filfiltro)s-1) && j==(%(columnfiltro)s-1)){
                            imagefiltred[ty * %(columna)s + tx] = 1;
                            a=0;  
                        }
                    }
                }
                else{
                    imagefiltred[ty * %(columna)s + tx] = 0;
                }
            }
        } 
    }  
}
"""
####################################################################################
kernel_code_template_dilatacion = """
__global__ void dilatacion(unsigned int *image, unsigned int *kernel, unsigned int *imagefiltred)
{
    int tx = threadIdx.x + blockDim.x * blockIdx.x;
    int ty = threadIdx.y + blockDim.y * blockIdx.y;
   
    int kernelRowRadius = (%(filfiltro)s-1)/2;
    int kernelColRadius = (%(columnfiltro)s-1)/2;

    if(ty<%(fila)s && tx<%(columna)s){
        int startRow= ty - kernelRowRadius;
        int startColumn= tx - kernelColRadius;
        for (int i=0; i<%(filfiltro)s; i++){
            for (int j=0; j<%(columnfiltro)s; j++){
                int currentRow = startRow + i;
                int currentCol = startColumn + j;
                if(currentRow>=0 && currentRow<%(fila)s && currentCol>=0 && currentCol<%(columna)s){                  
                    if(kernel[i * %(filfiltro)s +j]==1 && image[currentRow * %(columna)s + currentCol]==1){
                        imagefiltred[ty * %(columna)s + tx] = 1;
                    }
                    else{
                        
                    }
                }
                else{
                    imagefiltred[ty * %(columna)s + tx] = 0;
                }
            }
        } 
    }  
}
"""



img_array=np.array([[0,0,0,1,0,0,0],
                    [0,0,1,1,1,0,0],
                    [0,1,1,1,1,0,0],
                    [0,0,1,1,0,0,0],
                    [0,0,1,1,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0]])

image_in=img.imread("shingeki_gray.jpeg")

canalgrey = image_in[:,:,0]

filtro=np.array([[0,1,0,0,0],
                 [1,1,1,0,0],
                 [0,1,0,0,0],
                 [0,1,0,0,0],
                 [0,0,0,0,0]])

image= np.array(canalgrey).astype(np.uint32)
filtered=np.array(filtro).astype(np.uint32)

filas,columnas = canalgrey.shape
w1,w2= filtro.shape 

row2,column2=canalgrey.shape


treshold=150
binimage=np.zeros((row2,column2))


for row in range (row2):
    for column in range(column2):
        if canalgrey[row,column]<treshold:
            binimage[row,column]=0
        else:
            binimage[row,column]=1



binimage= np.array(binimage). astype(np.uint32)



img_gpu = cuda.mem_alloc(binimage.nbytes)
filtro_gpu = cuda.mem_alloc(filtered.nbytes)
filtered_gpu = cuda.mem_alloc(binimage.nbytes)
filtered_d_gpu = cuda.mem_alloc(binimage.nbytes)



i=int((w1-1)/2)
x=int(filas-i-1)

j=int((w2-1)/2)
y=int(columnas-j-1)

kernel_code_erosion = kernel_code_template_erosion% {
    'fila': filas, 
    'columna': columnas,
    'filfiltro':w1,
    'columnfiltro':w2,
    'i':i,
    'j':j
    }



kernel_code_dilatacion = kernel_code_template_dilatacion % {
    'fila': filas, 
    'columna': columnas,
    'filfiltro':w1,
    'columnfiltro':w2,
    'i':i,
    'j':j
    }

#print(kernel_code)


mod1 = compiler.SourceModule(kernel_code_erosion)

erosion = mod1.get_function("erosion")


mod2 = compiler.SourceModule(kernel_code_dilatacion)

dilatacion = mod2.get_function("dilatacion")



cuda.memcpy_htod(img_gpu, binimage)
cuda.memcpy_htod(filtro_gpu, filtered)

erosion(
    # inputs
    img_gpu,
    filtro_gpu,
    #output
    filtered_gpu, 
    # (only one) block of MATRIX_SIZE x MATRIX_SIZE threads
    block = (6,36, 1),
    grid = (100,8,1),
    )


gr= np.zeros((filas, columnas)).astype(np.uint32)
cuda.memcpy_dtoh(gr, filtered_gpu)
erosionada_gpu = cuda.mem_alloc(gr.nbytes)
cuda.memcpy_htod(erosionada_gpu, gr)

##################################################################

dilatacion(
    # inputs
    erosionada_gpu,
    filtro_gpu,
    #output
    filtered_d_gpu, 
    # (only one) block of MATRIX_SIZE x MATRIX_SIZE threads
    block = (6,36, 1),
    grid = (100,8,1),
    ) 

grd= np.zeros((filas, columnas)).astype(np.uint32)
cuda.memcpy_dtoh(grd, filtered_d_gpu)

print(image)

print('##################################################################')
print(gr)

figure, axes = plt.subplots(3)
axes[0].imshow(binimage,cmap='gray')
axes[1].imshow(gr,cmap='gray')
axes[2].imshow(grd,cmap='gray')
plt.show()

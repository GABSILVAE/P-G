import numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt
from numpy.core.records import array

from pycuda import compiler, gpuarray, tools
import pycuda.driver as cuda

# -- initialize the device
import pycuda.autoinit


kernel_code_template = """
__global__ void MatrixMulKernel(float *image, float *kernel, float *imagefiltred)
{
    int tx = threadIdx.x + blockDim.x * blockIdx.x;
    int ty = threadIdx.y + blockDim.y * blockIdx.y;
    
    if(ty < %(fila)s && tx < %(columna)s){

        int x = ((%(fila)s - %(i)s) - 1);
        int y = ((%(columna)s - %(j)s) - 1);

        for (int i=0; i<x; i++){

            for (int j=0; j<y; j++){

                int a = 0;

                for(int k=0; k<%(w1)s; k++){

                    for (int l=0; l<%(w2)s; l++){

                        if(kernel[k * %(w1)s + l]==1 && image[((i+k) * %(columna)s) + (j+l)]==0){

                            a = 1;
                        }
                        else{

                            if(a!=1 && k==2 && l==2){

                                imagefiltred[((i+1) * %(columna)s) + (j+1)] = 1;    
                            }
                        } 
                    }
               }
            }
        }

        imagefiltred[ty * %(columna)s + tx] = imagefiltred[(i+1) * %(columna)s) + (j+1)];
    }  
}
"""


'''
image=img.imread("shingeki_gray.jpeg")
canalgrey = image[:,:,0]
print(canalgrey.shape)
'''
img_array=np.array([[0,0,0,0,0,0,0],
                    [0,0,1,1,1,0,0],
                    [0,1,1,1,0,0,0],
                    [0,0,0,1,1,0,0],
                    [0,0,0,1,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0]])

image_in=img.imread("binarizada.jpeg")

print(image_in.shape)
canalgrey = image_in[:,:,0]
print(canalgrey.shape)

filtro=np.array([[0,0,0],
                [0,1,1],
                [0,0,0]]) 




image= np.array(canalgrey). astype(np.uint32)
filtered=np.array(filtro). astype(np.uint32)
print(image)
filas,columnas = canalgrey.shape
w1,w2= filtro.shape 

img_gpu = cuda.mem_alloc(image.nbytes)
filtro_gpu = cuda.mem_alloc(filtered.nbytes)
filtered_gpu = cuda.mem_alloc(image.nbytes)

i=int((w1-1)/2)
x=int(filas-i-1)

j=int((w2-1)/2)
y=int(columnas-j-1)

kernel_code = kernel_code_template % {
    'fila': filas, 
    'columna': columnas,
    'w1':w1,
    'w2':w2,
    'i':i,
    'j':j
    }

#print(kernel_code)


mod = compiler.SourceModule(kernel_code)

matrixmul = mod.get_function("MatrixMulKernel")


cuda.memcpy_htod(img_gpu, image)
cuda.memcpy_htod(filtro_gpu,filtered)

matrixmul(
    # inputs
    img_gpu,
    filtro_gpu,
    #output
    filtered_gpu, 
    # (only one) block of MATRIX_SIZE x MATRIX_SIZE threads
    block = (28,6, 1),
    grid = (10,100,1),
    ) 

gr= np.zeros((filas, columnas)).astype(np.uint32)


cuda.memcpy_dtoh(gr, filtered_gpu)

print('##################################################################')
print(gr)
'''
figure, axes = plt.subplots(2)
axes[0].imshow(canalgrey,cmap='gray')
axes[1].imshow(gr,cmap='gray')

plt.show()
'''
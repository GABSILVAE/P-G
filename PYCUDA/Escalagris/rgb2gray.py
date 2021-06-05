# Importacion de librerias
import numpy as np
import pycuda.autoinit
import pycuda.driver as cuda

from pycuda import compiler

# Definicion del kernel
kernel_code_template = """
    __global__ void rgb2gray(unsigned int *grayImage, unsigned int *rgbImage)
    {
        int x = threadIdx.x + blockIdx.x * blockDim.x;
        int y = threadIdx.y + blockIdx.y * blockDim.y;

        if(x < %(width)s && y < %(height)s){

            int grayOffset = y * %(width)s + x;
            int rgbOffset = grayOffset * %(channels)s;

            unsigned int r = rgbImage[rgbOffset];
            unsigned int g = rgbImage[rgbOffset + 1]; 
            unsigned int b = rgbImage[rgbOffset + 2];

            grayImage[grayOffset] = int((r + g + b) / 3); 
        }
    }
"""

def rgb2gray(image, height, width, channels=3):
    """
    Metodo para la conversion de RGB a escala de grises
    """
    # Asignacion de los tamanos de los vectores necesarios
    image_rgb_host = np.array(image).astype(np.float32)
    image_gray_host = np.zeros((height, width)).astype(np.float32)

    # Asignacion de memoria requerida dentro del procesamiento
    image_rgb_device = cuda.mem_alloc(image_rgb_host.nbytes)
    image_gray_device = cuda.mem_alloc(image_gray_host.nbytes)

    # Copia de la informacion a de la cpu a la gpu
    cuda.memcpy_htod(image_rgb_device, image_rgb_host)

    # Kernel modificado con los valores necesarios
    kernel_code = kernel_code_template % {
        'width': str(width),
        'height': str(height),
        'channels': str(channels)
    }

    rows_gpu = round(width/50)
    columns_gpu = round(height/20)

    print(rows_gpu,columns_gpu)

    # LLamdo del kernel
    mod = compiler.SourceModule(kernel_code)
    matrixmul = mod.get_function('rgb2gray')
    # Ejecucion del kernel
    matrixmul(
        image_gray_device,
        image_rgb_device, 
        block=(rows_gpu, columns_gpu,1),
        grid = (50,20,1)
    )

    #Copia de los resultados procesados por el kernel al cpu
    cuda.memcpy_dtoh(image_gray_host, image_gray_device)
    return image_gray_host
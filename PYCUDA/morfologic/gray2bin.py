import numpy as np
import pycuda.autoinit
import pycuda.driver as cuda

from pycuda import compiler, gpuarray

kernel_code_template = """
__global__ void gray2bin( float *grayimage, float *binimage)
{
    int tx = threadIdx.x + blockDim.x * blockIdx.x;
    int ty = threadIdx.y + blockDim.y * blockIdx.y;
    if(tx<%(width)s && ty< %(height)s){  
        int offsetgray = ty * %(width)s + tx;
        if(grayimage[offsetgray]<%(threshold)s){
            binimage[offsetgray]=0;
        }
        else{
            binimage[offsetgray]=1;
        }
    }
}
"""

def gray2bin(image_gray, height, width, threshold):
    """
    Method for converting an image grayscale to binarized
    """
    # Definition of necessary variables 
    rows_device = round(width/100)
    columns_device = round(height/100)

    # Assignment of variables within the host
    gray_cpu = np.array(image_gray).astype(np.float32)
    bin_cpu = np.zeros((height, width)).astype(np.float32)

    # Required memory allocation of the device, for variables
    gray_gpu = cuda.mem_alloc(gray_cpu.nbytes)
    bin_gpu = cuda.mem_alloc(bin_cpu.nbytes)

    # Copy data from host to device 
    cuda.memcpy_htod(gray_gpu, gray_cpu)

    # Kernel with the necessary values 
    kernel_code = kernel_code_template % {
        'height': height, 
        'width': width,
        'threshold': threshold
    }

    # Kernel call 
    mod = compiler.SourceModule(kernel_code)
    matrixmul = mod.get_function('gray2bin')
    
    # Kernel execution 
    matrixmul(
        # input
        gray_gpu,
        # output
        bin_gpu, 
        # (only one) block of MATRIX_SIZE x MATRIX_SIZE threads
        block = (rows_device, columns_device, 1),
        grid = (100,100,1),
    )

    # Copy the result to the host, hosted on the device
    cuda.memcpy_dtoh(bin_cpu, bin_gpu)
    return bin_cpu

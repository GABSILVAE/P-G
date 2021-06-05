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
''' DEFINITION OF THE METHOD OF CONVERTING THE GRICES SCALE IMAGE TO A BINARIZED IMAGE'''

def gray2bin(image_gray, height,width,threshold):
    image_gray_host = np.array(image_gray).astype(np.float32)
    image_bin_host = np.zeros((height, width)).astype(np.float32)
    
    image_gray_device = cuda.mem_alloc(image_gray_host.nbytes)
    image_bin_device = cuda.mem_alloc(image_bin_host.nbytes)

    cuda.memcpy_htod(image_gray_device, image_gray_host)

    kernel_code = kernel_code_template % {
    'height': height, 
    'width': width,
    'threshold': threshold
    }

    module = compiler.SourceModule(kernel_code)

    graytobin = module.get_function('gray2bin')
    graytobin(
        image_gray_device,
        image_bin_device, 
        block=(6,36, 1),
        grid = (100,8,1)
    )

    cuda.memcpy_dtoh(image_bin_host, image_bin_device)

    return image_bin_host

import numpy as np
import pycuda.autoinit
import pycuda.driver as cuda

from pycuda import compiler, gpuarray

kernel_code_template = """
__global__ void convolucion(float *image, float *kernel, float *imagefiltred)
{
    int tx = threadIdx.x + blockDim.x * blockIdx.x;
    int ty = threadIdx.y + blockDim.y * blockIdx.y;
    float accum=0;

    int kernelRowRadius = %(kernel_rows)s/2;
    int kernelColRadius = %(kernel_columns)s/2;

    if(ty < %(height)s && tx < %(width)s){

        int startRow= ty - kernelRowRadius;
        int startColumn= tx - kernelColRadius;

        for (int i=0; i<%(kernel_rows)s; i++){

            for (int j=0; j< %(kernel_columns)s; j++){

                int currentRow = startRow + i;
                int currentCol = startColumn + j;

                if(currentRow>=0 && currentRow < %(height)s && currentCol>=0 && currentCol < %(width)s){

                    accum+= image[(currentRow * %(width)s + currentCol)] * kernel[i * %(kernel_rows)s +j];
                }
                else{

                    accum=0;
                }


            }


        } 
        imagefiltred[ty * %(width)s + tx] = accum;
    }  

}
"""

''' 
definition of the methods for the selection of the kernel and its respective application '''

def conv(image,kernel):

   

    image_gray_host = np.array(image).astype(np.float32)
    kernel_host=np.array(kernel) .astype(np.float32)
   

    height,width =image_gray_host.shape
    kernel_rows,kernel_columns= kernel_host.shape

    image_filtered_host = np.zeros((height, width)).astype(np.float32)

    image_device = cuda.mem_alloc(image_gray_host.nbytes)
    kernel_device =cuda.mem_alloc(kernel_host.nbytes)
    image_filtered_device = cuda.mem_alloc(image_filtered_host.nbytes)

    cuda.memcpy_htod(image_device, image_gray_host)
    cuda.memcpy_htod(kernel_device, kernel_host)

    kernel_code = kernel_code_template % {
    'height': height, 
    'width': width,
    'kernel_rows':kernel_rows,
    'kernel_columns':kernel_columns
    }

    module = compiler.SourceModule(kernel_code)
    conv = module.get_function('convolucion')

    conv = module.get_function('convolucion')
    conv(
        image_device,
        kernel_device,
        image_filtered_device, 
        block=(6,36, 1),
        grid = (100,8,1)
    )
    


    cuda.memcpy_dtoh(image_filtered_host, image_filtered_device)

    return image_filtered_host


def seleccion_kernel (nombre):
   option = nombre
  
   if option == "laplace":
      kernel= np.array([[1,1,1],
                        [1,-8,1],
                        [1,1,1]])
      

   elif option == "convolucion":
         kernel= np.array([[0.04,0.04,0.04,0.04,0.04],
                [0.04,0.04,0.04,0.04,0.04],
                [0.04,0.04,0.04,0.04,0.04],
                [0.04,0.04,0.04,0.04,0.04],
                [0.04,0.04,0.04,0.04,0.04],])
        
         
   elif option == "gauss_a":
         kernel= np.array([[1,2,1],
                           [2,4,2],
                           [1,2,1]])
        
   
   elif option == "gauss_b":
         kernel= np.array([[1,4,6,4,1],
                           [4,16,24,16,4],
                           [6,24,36,24,6],
                           [4,16,24,16,4],
                           [1,4,6,4,1]]) 
         

   elif option == "gauss_c":
         kernel= np.array([[0,0,0],
                           [1,1,1],
                           [0,0,0]]) 
         

   elif option == "gauss_d":
         kernel= np.array([[1,0,0],
                           [0,1,0],
                           [0,0,1]])  
         

   
   elif option == "prewitt_a":
         kernel= np.array([[-1,-1,-1],    
                           [0,0,0],
                           [1,1,1]])  
         
         

   elif option == "prewitt_b":
         kernel= np.array([[-1,0,1],
                           [-1,0,1],
                           [-1,0,1]])  
        
         

   elif option == "prewitt_c":
      kernel= np.array([[0,1,1],
                        [-1,0,1],
                        [-1,-1,0]])
      
      
   
   elif option == "prewitt_d":
      kernel= np.array([[1,1,1],
                            [0,0,0],
                            [-1,-1,-1]])
      
         
         
   elif option == "roberts_a":
      kernel= np.array([[-1,0],
                        [0,1]])
      
      
         
   elif option == "roberts_b":
      kernel= np.array([[-1,0],
                       [1,0]])  
   


   elif option == "roberts_c":
      kernel= np.array([[-1,1],
                        [0,0]])
   return kernel

    
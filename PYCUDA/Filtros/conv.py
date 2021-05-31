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


def conv(image,kernel):

   

    image_cpu = np.array(image).astype(np.float32)
    kernel_cpu=np.array(kernel) .astype(np.float32)
   

    height,width =image_cpu.shape
    kernel_rows,kernel_columns= kernel_cpu.shape

    image_filtered_cpu = np.zeros((height, width)).astype(np.float32)

    image_gpu = cuda.mem_alloc(image_cpu.nbytes)
    kernel_gpu =cuda.mem_alloc(kernel_cpu.nbytes)
    image_filtered_gpu = cuda.mem_alloc(image_filtered_cpu.nbytes)

    cuda.memcpy_htod(image_gpu, image_cpu)
    cuda.memcpy_htod(kernel_gpu, kernel_cpu)

    kernel_code = kernel_code_template % {
    'height': height, 
    'width': width,
    'kernel_rows':kernel_rows,
    'kernel_columns':kernel_columns
    }

    mod = compiler.SourceModule(kernel_code)
    conv = mod.get_function('convolucion')

    conv = mod.get_function('convolucion')
    conv(
        image_gpu,
        kernel_gpu,
        image_filtered_gpu, 
        block=(6,36, 1),
        grid = (100,8,1)
    )
    


    cuda.memcpy_dtoh(image_filtered_cpu, image_filtered_gpu)

    return image_filtered_cpu



def seleccion_kernel (nombre):
   opcion = nombre
  
   if opcion == "laplace":
      kernel= np.array([[1,1,1],
                        [1,-8,1],
                        [1,1,1]])
      

   elif opcion == "convolucion":
         kernel= np.array([[0.04,0.04,0.04,0.04,0.04],
                [0.04,0.04,0.04,0.04,0.04],
                [0.04,0.04,0.04,0.04,0.04],
                [0.04,0.04,0.04,0.04,0.04],
                [0.04,0.04,0.04,0.04,0.04],])
        
         
   elif opcion == "gauss_a":
         kernel= np.array([[1,2,1],
                           [2,4,2],
                           [1,2,1]])
        
   
   elif opcion == "gauss_b":
         kernel= np.array([[1,4,6,4,1],
                           [4,16,24,16,4],
                           [6,24,36,24,6],
                           [4,16,24,16,4],
                           [1,4,6,4,1]]) 
         

   elif opcion == "gauss_c":
         kernel= np.array([[0,0,0],
                           [1,1,1],
                           [0,0,0]]) 
         

   elif opcion == "gauss_d":
         kernel= np.array([[1,0,0],
                           [0,1,0],
                           [0,0,1]])  
         

   
   elif opcion == "prewitt_a":
         kernel= np.array([[-1,-1,-1],    
                           [0,0,0],
                           [1,1,1]])  
         
         

   elif opcion == "prewitt_b":
         kernel= np.array([[-1,0,1],
                           [-1,0,1],
                           [-1,0,1]])  
        
         

   elif opcion == "prewitt_c":
      kernel= np.array([[0,1,1],
                        [-1,0,1],
                        [-1,-1,0]])
      
      
   
   elif opcion == "prewitt_d":
      kernel= np.array([[1,1,1],
                            [0,0,0],
                            [-1,-1,-1]])
      
         
         
   elif opcion == "roberts_a":
      kernel= np.array([[-1,0],
                        [0,1]])
      
      
         
   elif opcion == "roberts_b":
      kernel= np.array([[-1,0],
                       [1,0]])  
   


   elif opcion == "roberts_c":
      kernel= np.array([[-1,1],
                        [0,0]])
   return kernel
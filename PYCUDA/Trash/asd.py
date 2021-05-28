import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy

hilos = 10 

mod = SourceModule("""
  __global__ void suma(int *vector_1, int *vector_2, int *suma){
    int index =threadIdx.x + blockDim.x * blockIdx.x;
    
    suma[index]=vector_1[index]+vector_2[index];
    

  }
  """)


vector_1=numpy.array([0,1,2,3])
vector_1gpu= cuda.mem_alloc(vector_1.nbytes)

cuda.memcpy_htod(vector_1gpu,vector_1)


vector_2=numpy.array([4,4,5,7])

vector_2gpu= cuda.mem_alloc(vector_2.nbytes)

cuda.memcpy_htod(vector_2gpu,vector_2)

suma = numpy.zeros_like(vector_1)

sumagpu= cuda.mem_alloc(suma.nbytes)
cuda.memcpy_htod(sumagpu,suma)



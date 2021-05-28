import numpy
import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule

mod = SourceModule("""
	__global__ void mult(int *a, int *b, int *c){

        int idx =  threadIdx.x;
        int idy =  threadIdx.y;
		int i = idy * 6 + idx;

        int sum=0;

        for (int j = 0; j< 6 ;j++){
            sum += a[idy * 6 +j] * b[j * 6 + idx];
        }
        c[i]= 8;
	}
""")

mult = mod.get_function("mult")

filas = 6
columnas = 6
a = numpy.ones((filas, columnas))

b = numpy.ones((filas, columnas))

d= numpy.zeros_like(a)

mult(drv.Out(d), drv.In(a),drv.In(b), block = (6,6,1), grid = (1,1))

print(a)
print('****************************************************')
print(b)
print('****************************************************')
print(d)
	
	
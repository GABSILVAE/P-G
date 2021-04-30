import pycuda.autoinit
import pycuda.driver as drv
import pycuda.gpuarray as gpuarray

import numpy
a = numpy.ones(400, dtype = numpy.float32)
a_gpu = gpuarray.to_gpu(a)

ans = (2*a_gpu).get()

print(ans)
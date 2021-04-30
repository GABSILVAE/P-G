import pycuda.autoinit
import pycuda.driver as drv
import pycuda.gpuarray as gpuarray

import numpy
a = numpy.ones(400, dtype = numpy.float32)
a_gpu = gpuarray.to_gpu(a)

ans = (2*a_gpu).get()

print(ans)


b = numpy.matrix([1,2,3,4])
b_gpu = gpuarray.to_gpu(b)

c = numpy.matrix([1,2,3,4])
c_gpu = gpuarray.to_gpu(c)

res = b_gpu + c_gpu
ans = res.get()

print(ans)
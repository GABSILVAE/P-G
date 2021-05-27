///////////////////////////////////////////////////////////////////////////
// PROGRAMACIÓN EN CUDA C/C++
// Curso Basico
// Agosto 2020
///////////////////////////////////////////////////////////////////////////
//
///usr/local/cuda/bin/nvcc Basico2.cu -o test
//./test
//
// includes
#include<stdio.h>
#include<stdio.h>
#include<cuda_runtime.h>
#define filas 3
#define columnas 3

__global__ void add(int *a, int *b, int *c) {

	int x = blockIdx.x * blockDim.x + threadIdx.x;
	int y = blockIdx.y * blockDim.y + threadIdx.y;
	int i = (columnas * y) + x;
	if(y<filas && x< columnas)
	{
		c[i] = a[i] + b[i];
	}
}	


int main() {

	int *hst_a, *hst_b, *hst_c;
	int *dev_a, *dev_b, *dev_c;

	hst_a=(int*)malloc(filas *columnas * sizeof(int));
	hst_b=(int*)malloc(filas *columnas * sizeof(int));
	hst_c=(int*)malloc(filas *columnas * sizeof(int));


	
	cudaMalloc((void**)&dev_a, filas *columnas * sizeof(int));
	cudaMalloc((void**)&dev_b, filas *columnas * sizeof(int));
	cudaMalloc((void**)&dev_c, filas *columnas * sizeof(int));


	 for (int i = 0; i < filas; i++) {
		int cont = 0;
		for (int j = 0; j < columnas; j++) {
			hst_a[i * columnas+j]=1;
			hst_b[i * columnas+j]=2;
   			cont++;
  		}
 	}



	cudaMemcpy(dev_a, hst_a, filas * columnas * sizeof(int),cudaMemcpyHostToDevice);
	cudaMemcpy(dev_b, hst_b, filas * columnas * sizeof(int),cudaMemcpyHostToDevice);



	dim3 grid(columnas, filas);

	add<<<grid, 2>>>(dev_a, dev_b, dev_c);

	cudaMemcpy(hst_c, dev_c, filas * columnas * sizeof(int), cudaMemcpyDeviceToHost);

	for (int y = 0; y < filas; y++)
	{
		for (int x = 0; x < columnas; x++) {
			printf("%3d ", hst_c[x + y*columnas]);
		}
  		printf("\n");
 	}
	return 0;


}

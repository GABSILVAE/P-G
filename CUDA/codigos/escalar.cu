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

__global__ void mult(int *a, int *num, int *b){

	int idx= blockIdx.x * blockDim.x + threadIdx.x;
	int idy= blockIdx.y * blockDim.y + threadIdx.y;
	int i = (columnas * idy) + idx;

	if(idy<filas && idx< columnas){

		b[i]=num[0] * a[i];	
	}

	


}


int main (int argc, char** argv)
{

	int *hst_a, *hst_num, *hst_b;

	int *dev_a, *dev_b, *dev_num;

	hst_a=(int*)malloc(filas*columnas *sizeof(int));
	hst_num=(int*)malloc(1 *sizeof(int)); 
	hst_b=(int*)malloc(filas*columnas *sizeof(int));



	cudaMalloc((void**)&dev_a , filas*columnas * sizeof(int));
	cudaMalloc((void**)&dev_num , 1 * sizeof(int));
	cudaMalloc((void**)&dev_b , filas*columnas * sizeof(int));

	hst_num[0]=5;

	for (int i = 0; i < filas; i++) {
		
		for (int j = 0; j < columnas; j++) {
			hst_a[i * columnas+j]=1;
			hst_b[i * columnas+j]=0;
   			
  		}
 	}


	cudaMemcpy(dev_a, hst_a, filas * columnas * sizeof(int),cudaMemcpyHostToDevice);
	cudaMemcpy(dev_num, hst_num, 1 * sizeof(int),cudaMemcpyHostToDevice);

	dim3 grid(columnas, filas);

	mult<<<grid, 1>>>(dev_a, dev_num, dev_b);


	cudaMemcpy(hst_b, dev_b, filas * columnas * sizeof(int), cudaMemcpyDeviceToHost);

	
	for (int y = 0; y < filas; y++)
	{
		for (int x = 0; x < columnas; x++) {
			printf("%3d ", hst_a[x + y*columnas]);
		}
  		printf("\n");
 	}


	for (int y = 0; y < filas; y++)
	{
		for (int x = 0; x < columnas; x++) {
			printf("%3d ", hst_b[x + y*columnas]);
		}
  		printf("\n");
 	}


	// salida del programa
	printf("\n<pulsa [INTRO] para finalizar>\n");
	getchar();
	return 0;










}

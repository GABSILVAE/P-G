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

__global__ void suma(int *c, int *a, int *b, int filas, int columnas)
{
	int x = blockIdx.x * blockDim.x + threadIdx.x;
 	int y = blockIdx.y * blockDim.y + threadIdx.y;
 	int i = (columnas * y) + x;

 	c[i] = a[i] + b[i];


}

int main (int argc, char** argv)
{
	int a[filas][columnas], b[filas][columnas], c[filas][columnas];
	int *dev_a, *dev_b, *dev_c;
	int filas=3;
	int columnas=3;
	int n=filas * columnas;





	hst_a=(int*)malloc(n * sizeof(int));
	hst_b=(int*)malloc(n * sizeof(int));
	hst_c=(int*)malloc(n * sizeof(int));

	cudaMalloc((void**)&dev_a, n * sizeof(int));
	cudaMalloc((void**)&dev_b, n * sizeof(int));
	cudaMalloc((void**)&dev_c, n * sizeof(int));


	for (int i=0;i<filas;i++)
	{
		for(int j=0;j<columnas;j++)
		{
			hst_a[i * columnas+j]=1;
			hst_b[i * columnas+j]=2;		
		}
	}



	dim3 Nbloques(1);
	dim3 hilosb(columnas, filas);

	cudaMemcpy(dev_a, hst_a, n * sizeof(int), cudaMemcpyHostToDevice);
	cudaMemcpy(dev_b, hst_b, n * sizeof(int), cudaMemcpyHostToDevice);

	suma <<<Nbloques,hilosb>>> (dev_a,dev_b,dev_c,filas,columnas);
	
	cudaMemcpy(hst_c, dev_c, n*sizeof(int), cudaMemcpyDeviceToHost);

	
	printf("> Matriz a:\n");
	for (int i = 0; i<filas; i++)
	{
		for (int j = 0; j<columnas; j++)
		{
			printf("%3d ", hst_a[j + i*columnas]);
		}
		printf("\n");
	}


	


	printf("> Matriz b:\n");
	for (int i = 0; i<filas; i++)
	{
		for (int j = 0; j<columnas; j++)
		{
			printf("%3d ", hst_b[j + i*columnas]);
		}
		printf("\n");
	}


	printf("> Matriz c:\n");
	for (int i = 0; i<filas; i++)
	{
		for (int j = 0; j<columnas; j++)
		{
			printf("%3d ", hst_c[j + i*columnas]);
		}
		printf("\n");
	}





}

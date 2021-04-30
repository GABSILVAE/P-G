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
#define hilos 9

__global__ void mult(int *a, int *b, int *c, int columnas, int filas )
{

	int idy =  blockIdx.y * blockDim.y + threadIdx.y;
	int idx =  blockIdx.x * blockDim.x + threadIdx.x;
	int i =  idy * columnas + idx;
	
	if(idy<filas && idx <columnas){

		int sum=0;
		for(int j = 0; j<columnas ; j++){
			
			sum+= a[idy * columnas +j] * b[j * columnas + idx];
		}
		c[i]= sum;
	} 

	

}


int main(int argc, char ** argv)
{


	int *hst_a, *hst_b, *hst_c;
	
	int *dev_a, *dev_b, *dev_c;
	
	int filas=640;
	int columnas=480;

	int n = filas*columnas; 
	
	hst_a=(int*)malloc(n *sizeof(int));
	hst_b=(int*)malloc(n *sizeof(int)); 
	hst_c=(int*)malloc(n *sizeof(int));


	cudaMalloc((void**)&dev_a, n * sizeof(int));
	cudaMalloc((void**)&dev_b, n * sizeof(int));
	cudaMalloc((void**)&dev_c, n * sizeof(int));


	for (int i = 0; i < filas; i++) {
		
		for (int j = 0; j < columnas; j++) {
			hst_a[i * columnas+j]=1;
			hst_b[i * columnas+j]=2;
   			
  		}
 	}

	cudaMemcpy(dev_a, hst_a,n * sizeof(int),cudaMemcpyHostToDevice);
	cudaMemcpy(dev_b, hst_b,n * sizeof(int),cudaMemcpyHostToDevice);


	
	dim3 grid(columnas, filas);

	

	printf("matrices  de %d elementos\n", n);

	

	mult<<<grid, 6>>> (dev_a,dev_b,dev_c,filas,columnas);


	cudaMemcpy(hst_c, dev_c, n * sizeof(int), cudaMemcpyDeviceToHost);

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


	for (int y = 0; y < filas; y++)
	{
		for (int x = 0; x < columnas; x++) {
			printf("%3d ", hst_c[x + y*columnas]);
		}
  		printf("\n");
 	}


	// salida del programa
	printf("\n<pulsa [INTRO] para finalizar>\n");
	getchar();
	return 0;



}

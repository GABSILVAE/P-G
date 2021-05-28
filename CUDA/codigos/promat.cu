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

__global__ void prom(int *a, int *dato,int filas , int columnas, int n){

	int idy =  blockIdx.y * blockDim.y + threadIdx.y;
	int idx =  blockIdx.x * blockDim.x + threadIdx.x;
	//int i = (columnas * idy) + idx;
	
	if(idy<filas && idx <columnas){

		int sum=0;
		for(int j = 0; j<n ; j++){
			
			sum+= a[j];
		}
		dato[0]= sum/n;
	} 




}


int main (int argc, char** argv){


	int *hst_a, *hst_dato;
	int *dev_a, *dev_dato;

	int filas=6;
	int columnas=6;

	int n = filas*columnas;


	
	hst_a=(int*)malloc(n *sizeof(int));
	hst_dato=(int*)malloc(1 *sizeof(int));


	cudaMalloc((void**)&dev_a, n * sizeof(int));
	cudaMalloc((void**)&dev_dato , 1 * sizeof(int));



	for (int i = 0; i < filas; i++) {
		
		for (int j = 0; j < columnas; j++) {
			hst_a[i * columnas+j]=1;
			
  		}
 	}

	cudaMemcpy(dev_a, hst_a, n * sizeof(int),cudaMemcpyHostToDevice);
 
	dim3 grid(columnas, filas);

	prom<<<grid, 1>>>(dev_a, dev_dato,filas, columnas,n);

	cudaMemcpy(hst_dato,dev_dato,1*sizeof(int), cudaMemcpyDeviceToHost);



	for (int y = 0; y < filas; y++)
	{
		for (int x = 0; x < columnas; x++) {
			printf("%3d ", hst_a[x + y*columnas]);
		}
  		printf("\n");
 	}



	printf("vector resultado:\n");

	printf("%d",hst_dato[0]);



	
	// salida del programa
	printf("\n<pulsa [INTRO] para finalizar>\n");
	getchar();
	return 0;


}

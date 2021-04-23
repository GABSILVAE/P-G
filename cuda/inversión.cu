#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>

__global__ void inversion(int *vector_1, int *vector_2, int n)
{
	int index= threadIdx.x;
	vector_1[index]=index;
	vector_2[index]=vector_1[((n-1)-index)];
}

int main (int argc, char** argv){
	
	
	// declaraciones
	int *hst_vector_1, *hst_vector_2;
	int *dev_vector_1, *dev_vector_2;
	int n=8;
	
	// reserva de memoria  en el host
	hst_vector_1=(int*)malloc(n*sizeof(int));
	hst_vector_2=(int*)malloc(n*sizeof(int));
	
	// reserva de memoria en el device
	cudaMalloc ((void**)&dev_vector_1, n*sizeof(int));
	cudaMalloc ((void**)&dev_vector_2, n*sizeof(int));
	
	// inicialización de los vectore en el host
	for (int i=0; i<n; i++){
		
		hst_vector_1[i]=0;
		hst_vector_2[i]=0;
		
	}
	
	// copia de los datos
	
	inversion <<<1,n>>> (dev_vector_1, dev_vector_2, n);
	
	// envio de datos del device a host
	
	cudaMemcpy(hst_vector_1,dev_vector_1, n*sizeof(int), cudaMemcpyDeviceToHost);
	cudaMemcpy(hst_vector_2,dev_vector_2, n*sizeof(int), cudaMemcpyDeviceToHost);}

	// imprimiendo los datos
	
	printf ("VECTOR1: \n");
	for(int i=0; i<0; i++){
		
		printf("%2d", hst_vector_1[i]);
	}
	
	printf("\n");
	
	printf("VECTOR2: \n")
	
	for(int i=0; i< n; i++){
		
		printf("2%d", hst_vector_2[i]);
		
		
	}
	
	return 0;
	
}

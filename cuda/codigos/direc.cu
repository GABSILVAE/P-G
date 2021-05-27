#include<stdio.h>
#include<stdlib.h>
#include<cuda_runtime.h>

#define hilos 100

__global__ void dir (int *in,int *out,int n){
	
	int index= threadIdx.x +blockDim.x *blockIdx.x;
	

	if (index<n){
		
		out[0]=2 * in[0];
	}	
}


int main(int argc, char** argv)
{
	int *hst_in, *hst_out;
	int *dev_in, *dev_out;
	int n=10;

	hst_in=(int*)malloc(1*sizeof(int));
	hst_out=(int*)malloc(1*sizeof(int));
	


	cudaMalloc((void**)&dev_in,1*sizeof(int));
	cudaMalloc((void**)&dev_out,1*sizeof(int));


	hst_in[0]=2;

	cudaMemcpy(dev_in,hst_in,1*sizeof(int), cudaMemcpyHostToDevice);
 
	int bloques = n/hilos;
	
	if(n%hilos !=0){

		bloques=bloques+1;
	}


	printf("vector de %d elementos\n", n);

	printf("lanzamiento  con %d bloques de %d hilos(%d elementos)\n",bloques,hilos,n);

	dir<<<bloques, hilos>>> (dev_in,dev_out,n);

	cudaMemcpy(hst_in,dev_in,1*sizeof(int), cudaMemcpyDeviceToHost);
	cudaMemcpy(hst_out,dev_out,1*sizeof(int), cudaMemcpyDeviceToHost);




	printf("in:\n");
	
	printf("%d \n",hst_in[0]);


	printf("out:\n");
	
	printf("%d \n",hst_out[0]);


	printf("\n");
	// salida
	printf("***************************************************\n");
	printf("<pulsa [INTRO] para finalizar>");
	getchar();
	return 0;





  	
} 

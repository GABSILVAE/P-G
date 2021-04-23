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

#define hilos 10 // numero de hilos por bloque 

__global__ void suma(int *vector_1, int *dato, int n){

	// kernel multibloque 
	// identificaador global de cada hilo en el bloque 
	int index =threadIdx.x + blockDim.x * blockIdx.x;
	vector_1[index] = index;
	//truncamiento de los hilos solo trabajan los hilos nesesarios 
	if(index<n)
	{
		int sum=0;
		for(int i=0;i<n;i++){
			sum += vector_1[i];
		}
		dato[0]=sum;
	}

}

///////////////////////////////////
int main (void)
{	
	
	// declaraiones 
	
	int *hst_vector1, *hst_dato;
	
	int *dev_vector1, *dev_dato;

	int n=5;
	
	// reserva en el host
	hst_vector1=(int*)malloc(n*sizeof(int));
	hst_dato=(int*)malloc(1*sizeof(int));
	
	
	// reserva en el device	
	cudaMalloc((void**)&dev_vector1,n * sizeof(int));
	cudaMalloc((void**)&dev_dato,1 * sizeof(int));
	


	
	for(int i=0; i<n; i++)
	{
		hst_vector1[i]=0;
		
	}

	// envio de datos al device 
	//cudaMemcpy(dev_vector1,hst_vector1,n *sizeof(int), cudaMemcpyHostToDevice);
	
	//lanzamiento del kernel 
	// calculo del numero de bloques

	int bloques = n/hilos;

	if (n%hilos !=0)
	{	
	
		bloques=bloques+1;
	}

	printf("vector de %d elementos\n", n);

	printf("lanzamiento  con %d bloques de %d hilos(%d elementos)\n",bloques,hilos,n);

	suma<<<bloques, hilos>>> (dev_vector1,dev_dato,n);

	// captura de los datos del device

	cudaMemcpy(hst_vector1,dev_vector1,n*sizeof(int), cudaMemcpyDeviceToHost);
	cudaMemcpy(hst_dato,dev_dato,1*sizeof(int), cudaMemcpyDeviceToHost);

	/*printf("vector1:\n");
	
	
	
	for(int i=0; i<n; i++)
	{
		
		printf("%d",hst_vector1[i]);
	
	}
	*/
	
	printf("vector resultado:\n");

	printf("%d",hst_dato[0]);
	
	

	printf("\n");
	// salida
	printf("***************************************************\n");
	printf("<pulsa [INTRO] para finalizar>");
	getchar();
	return 0;

}

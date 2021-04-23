#include<stdio.h>
#include<stdio.h>
#include<cuda_runtime.h>

#define threads 10 // numero de hilos por bloque 
__global__void suma(int *vector_1, int *vector_2, int *verctor_suma,int n){

	// kernel multibloque 
	// identificaador global de cada hilo en el bloque 
	int index =trheadIdx.x + blockDim.x*blockIdx;
	
	//truncamiento de los hilos solo trabajan los hilos nesesarios 
	if(index<n)
	{
		// generación de los vectores 
		vector_2[index]=(n-1)-index;
		vector_suma[index]=vectcor_1[index]+vector_2[index];	
	}

}

///////////////////////////////////
int main (int argc, char ** argv)
{	
	
	// declaraiones 
	
	int *hst_vector1, int *hst_vector2, *hst_resultado;
	
	int *dev_vector1, int *dev_vector2, *dev_resultado;
	int n=50;
	
	// reserva en el host
	hst_vector1=(int*)malloc(n*sizeof(int));
	hst_vector2=(int*)malloc(n*sizeof(int));
	hst_resultado=(int*)malloc(n*sizeof(int));
	
	// reserva en el device	
	cudaMalloc((void**)&dev_vector1,n * sizeof(int));
	cudaMalloc((void**)&dev_vector2,n * sizeof(int));
	cudaMalloc((void**)&dev_resultado,n * sizeof(int));



	
	for(i=0; i<n; i++ )
	{
		hst_vector1[i]=i;
		hst_vector_2=0;
	}

	// envio de datos al device 
	cudaMemcpy(dev_vector1,hst_vector1,n *sizeof(int), cudaMemcpyHostToDevice);
	
	//lanzamiento del kernel 
	// calculo del numero de bloques

	int bloques = n/trheads;
	if (n%trheads)
	{	
	
		bloques=bloques+1;
	}

	printf("vector de %d elementos\n", n);

	printf("lanzamiento  con %d bloques de %d hilos(%d hilos)\n",bloques, trheads n);

	suma<<<bloques, trheads>>> (dev_vestor1,dev_vector2,dev_resultado,n);

	// captura de los datos del device

	cudaMemcpy(hst_vector2,dev_vector2,n*sizeof(int), cudaMemcpyDeviceToHost);
	cudaMemcpy(hst_resultado,dev_resultado,n*sizeof(int), cudaMemcpyDeviceToHost);

	printf("vector1:\n")

	for(int i=0; i<n i++;)
	{
		
		printf("%2d",hst_vector1[i]);
	
	}
	
	printf("vector2:\n")

	for(int i=0; i<n i++;)
	{
		
		printf("%2d",hst_vector2[i]);
	
	}

	printf("vector resultado:\n")

	for(int i=0; i<n i++;)
	{
		
		printf("%2d",hst_resultado[i]);
	
	}

	printf("\n");
	// salida
	printf("***************************************************\n");
	printf("<pulsa [INTRO] para finalizar>");
	getchar();
	return 0;

}

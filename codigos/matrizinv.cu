///////////////////////////////////////////////////////////////////////////
// PROGRAMACIÓN EN CUDA C/C++
// Curso Basico
// Agosto 2020
///////////////////////////////////////////////////////////////////////////
// includes
#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>
// defines
#define COLUMNAS 20 // Numero de columnas -> eje x
#define FILAS 12     // Numero de filas    -> eje y


__global__ void nodiag_normalize(float *A, float *I, int n , int i)
{
	// KERNEL BIDIMENSIONAL: (X,Y)
	// indice de columna: EJE x
	int x =blockIdx.x * blockDim.x + threadIdx.x;
	// indice de fila: EJE y
	int y =  blockIdx.y * blockDim.y + threadIdx.y;	
	
	if (x<n && y<n){
		
	if ( x == i && x!=y){
			
		I[x*n + y ] /= A[i*n + i];
		A[x*n + y] /= A[i*n +i];
	}
	}
}




__global__ void diag_normalize(float *A, float *I, int n , int i)
{
	// KERNEL BIDIMENSIONAL: (X,Y)
	// indice de columna: EJE x
	int x =blockIdx.x * blockDim.x + threadIdx.x;
	// indice de fila: EJE y
	int y =  blockIdx.y * blockDim.y + threadIdx.y;	
	
	if (x<n && y<n){
		
	if ( x == y && x==i){
			
		I[x*n + y ] /= A[i*n + i];
		A[x*n + y] /= A[i*n + i];
	}

	}
}






__global__ void gaussjordan(float *A, float *I, int n , int i)
{
	// KERNEL BIDIMENSIONAL: (X,Y)
	// indice de columna: EJE x
	int x =blockIdx.x * blockDim.x + threadIdx.x;
	// indice de fila: EJE y
	int y =  blockIdx.y * blockDim.y + threadIdx.y;	
	
	if (x<n && y<n){
		
		if ( x != i ){

			I[x*n + y ] -= I[i*n + i] * A[x*n +i];

			if(y !=i){

				A[x*n + y] -= A[i*n + i] * A[x*n +i];
			}

		}

	}
}



__global__ void set_zero(float *A, float *I, int n , int i)
{
	// KERNEL BIDIMENSIONAL: (X,Y)
	// indice de columna: EJE x
	int x =blockIdx.x * blockDim.x + threadIdx.x;
	// indice de fila: EJE y
	int y =  blockIdx.y * blockDim.y + threadIdx.y;	
	
	if (x<n && y<n){
		
		if ( x != i ){

			I[x*n + y ] -= I[i*n + i] * A[x*n +i];

			if(y ==i){

				A[x*n + y] = 0;
			}

		}

	}
}


///////////////////////////////////////////////////////////////////////////
int main(int argc, char** argv)
{
	// declaraciones
	float *hst_A, *hst_I;
	float *dev_A, *dev_I;
	
	int n =3;

	// reserva en el host
	hst_A = (float*)malloc(n*n * sizeof(float));
	hst_I = (float*)malloc(n*n * sizeof(float));
	
	//float d[n][n]={{1.0,2.0,3.0},{4.0,5.0,6.0},{7.0,8.0,9.0}};

	// reserva en el device
	cudaMalloc((void**)&dev_A,  n*n* sizeof(float));
	cudaMalloc((void**)&dev_I, n*n * sizeof(float));

	// incializacion
	for (int i = 1; i<9; i++)
	{
		hst_A[i] = i+1; // numeros consecutivos comenzando desde el 1
		hst_I[i] = 0;
	}

	// dimensiones del kernel
	// 1 Bloque
	dim3 Nbloques(1,1);
	
	// bloque bidimensional (x,y)
	// Eje x-> COLUMNAS
	// Eje y-> FILAS
	dim3 hilosB(3,3);

	// copia de datos hacia el device
	cudaMemcpy(dev_A, hst_A, n*n * sizeof(float), cudaMemcpyHostToDevice);

	for(int i=0; i<n; i++){

		nodiag_normalize <<<Nbloques, hilosB >>>(dev_A, dev_I,n ,i);
		diag_normalize <<<Nbloques, hilosB >>>(dev_A, dev_I,n ,i);
		gaussjordan <<<Nbloques, hilosB >>>(dev_A, dev_I,n ,i);
		set_zero <<<Nbloques, hilosB >>>(dev_A, dev_I,n ,i);



	}

	// llamada al kernel
	

	// recogida de datos desde el device
	cudaMemcpy(hst_I, dev_I, n * sizeof(float), cudaMemcpyDeviceToHost);

	// impresion de resultados
	printf("> MATRIZ ORIGINAL:\n");
	for (int i = 0; i<n; i++)
	{
		for (int j = 0; j<n; j++)
		{
			printf("%f ", hst_A[j + i*n]);
		}
		printf("\n");
	}
	printf("\n");
	printf("> MATRIZ FINAL:\n");
	for (int i = 0; i<n; i++)
	{
		for (int j = 0; j<n; j++)
		{
			printf("%f ", hst_I[j + i*n]);
		}
		printf("\n");
	}

	// salida del programa
	printf("\n<pulsa [INTRO] para finalizar>\n");
	getchar();
	return 0;
}

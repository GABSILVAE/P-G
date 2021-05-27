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
#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>

__global__ void suma(int *vector_1, int *vector_2, int *vector_suma, int n)
{
	// identificador de hilo
	int myID = threadIdx.x;
	// generamos el vector 2
	vector_2[myID] = (n - 1) - myID;
	// escritura de resultados
	vector_suma[myID] = vector_1[myID] + vector_2[myID];
}

int main(int argc, char** argv)
{
	// declaraciones
	int *hst_vector1, *hst_vector2, *hst_resultado;
	int *dev_vector1, *dev_vector2, *dev_resultado;
	int n = 8;
	
	// reserva en el host
	hst_vector1 = (int*)malloc(n * sizeof(int));
	hst_vector2 = (int*)malloc(n * sizeof(int));
	hst_resultado = (int*)malloc(n * sizeof(int));

	// reserva en el device
	cudaMalloc((void**)&dev_vector1, n * sizeof(int));
	cudaMalloc((void**)&dev_vector2, n * sizeof(int));
	cudaMalloc((void**)&dev_resultado, n * sizeof(int));

	// inicializacion de vectores
	for (int i = 0; i < n; i++)
	{
		hst_vector1[i] = i;
		hst_vector2[i] = 0;
	}

	// copia de datos hacia el device
	cudaMemcpy(dev_vector1, hst_vector1, n * sizeof(int), cudaMemcpyHostToDevice);

	// LANZAMIENTO DEL KERNEL
	suma <<< 1, n >>>(dev_vector1, dev_vector2, dev_resultado, n);

	// recogida de datos desde el device
	cudaMemcpy(hst_vector2, dev_vector2, n * sizeof(int), cudaMemcpyDeviceToHost);
	cudaMemcpy(hst_resultado, dev_resultado, n * sizeof(int), cudaMemcpyDeviceToHost);

	// impresion de resultados
	printf("VECTOR 1:\n");
	for (int i = 0; i < n; i++)
	{
		printf("%2d ", hst_vector1[i]);
	}
	printf("\n");
	printf("VECTOR 2:\n");
	for (int i = 0; i < n; i++)
	{
		printf("%2d ", hst_vector2[i]);
	}
	printf("\n");
	printf("SUMA:\n");
	for (int i = 0; i < n; i++)
	{
		printf("%2d ", hst_resultado[i]);
	}
	printf("\n");
	// salida
	printf("***************************************************\n");
	printf("<pulsa [INTRO] para finalizar>");
	getchar();
	return 0;
}
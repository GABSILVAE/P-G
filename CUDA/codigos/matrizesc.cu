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
#define COLUMNAS 3 // Numero de columnas -> eje x
#define FILAS 3     // Numero de filas    -> eje y

__global__ void MatFinal(int *a, int *num, int *c)
{
	// KERNEL BIDIMENSIONAL: (X,Y)
	// indice de columna: EJE x
	int columna = threadIdx.x;
	// indice de fila: EJE y
	int fila = threadIdx.y;
	// KERNEL DE UN SOLO BLOQUE:
	// indice lineal
	int globalID = columna + fila * COLUMNAS;
	
	// Escritura en la matriz final
	c[globalID] = num[0] *a [globalID];
}
///////////////////////////////////////////////////////////////////////////
int main(int argc, char** argv)
{
	// declaraciones
	int *hst_a, *hst_c, *hst_num;
	int *dev_a, *dev_c, *dev_num;

	// reserva en el host
	hst_a = (int*)malloc(FILAS*COLUMNAS * sizeof(int));
	hst_num = (int*)malloc(1* sizeof(int));
	hst_c = (int*)malloc(FILAS*COLUMNAS * sizeof(int));

	// reserva en el device
	cudaMalloc((void**)&dev_a, FILAS*COLUMNAS * sizeof(int));
	cudaMalloc((void**)&dev_num, 1 * sizeof(int));
	cudaMalloc((void**)&dev_c, FILAS*COLUMNAS * sizeof(int));

	hst_num[0]=3;

	// incializacion
	for (int i = 0; i<FILAS*COLUMNAS; i++)
	{
		hst_a[i] = 1; // numeros consecutivos comenzando desde el 1
		
	}

	// dimensiones del kernel
	// 1 Bloque
	dim3 Nbloques(1);
	
	// bloque bidimensional (x,y)
	// Eje x-> COLUMNAS
	// Eje y-> FILAS
	dim3 hilosB(COLUMNAS, FILAS);

	// copia de datos hacia el device
	cudaMemcpy(dev_a, hst_a, FILAS*COLUMNAS * sizeof(int), cudaMemcpyHostToDevice);
	cudaMemcpy(dev_num, hst_num, 1 * sizeof(int), cudaMemcpyHostToDevice);
	
	// Numero de hilos
	printf("> KERNEL de 1 BLOQUE con %d HILOS:\n", COLUMNAS*FILAS);
	printf("  eje x -> %2d hilos\n  eje y -> %2d hilos\n", COLUMNAS, FILAS);

	// llamada al kernel
	MatFinal <<<Nbloques, hilosB >>>(dev_a, dev_num, dev_c);

	// recogida de datos desde el device
	cudaMemcpy(hst_c, dev_c, FILAS*COLUMNAS * sizeof(int), cudaMemcpyDeviceToHost);

	// impresion de resultados
	printf("> Matriz a:\n");
	for (int i = 0; i<FILAS; i++)
	{
		for (int j = 0; j<COLUMNAS; j++)
		{
			printf("%3d ", hst_a[j + i*COLUMNAS]);
		}
		printf("\n");
	}

	 

	printf("\n");
	printf("> Matriz c:\n");
	for (int i = 0; i<COLUMNAS; i++)
	{
		for (int j = 0; j<FILAS; j++)
		{
			printf("%3d ", hst_c[j + i*COLUMNAS]);
		}
		printf("\n");
	}





	// salida del programa
	printf("\n<pulsa [INTRO] para finalizar>\n");
	getchar();
	return 0;
}

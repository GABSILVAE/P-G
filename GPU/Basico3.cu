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
#define BLOCK 10 // Lanzamiento con bloques de 'BLOCK' hilos

__global__ void suma(int *vector_1, int *vector_2, int *vector_suma, int n)
{
	// KERNEL 'MULTIBLOQUE'
	// identificador global de cada hilo
	int myID = threadIdx.x + blockDim.x * blockIdx.x;
	// solo trabajan n hilos
	// el resto no debe hacer nada
	if (myID < n)
	{
		// generamos el vector 2
		vector_2[myID] = (n - 1) - myID;
		
		// escritura de resultados
		vector_suma[myID] = vector_1[myID] + vector_2[myID];
	}
}
int main(int argc, char** argv)
{
	// declaraciones
	int *hst_vector1, *hst_vector2, *hst_resultado;
	int *dev_vector1, *dev_vector2, *dev_resultado;
	int n = 25;

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
	// calculamos el numero de bloques
	int bloques = n / BLOCK;
	if (n%BLOCK != 0)
		// Si el tamaño del vector no es multiplo del tamaño del bloque
		// lanzamos un bloque completo adicional
	{
		bloques = bloques + 1;
	}

	printf("> Vector de %d elementos\n", n);
	printf("> Lanzamiento con %d bloques de %d hilos (%d hilos)\n", bloques, BLOCK, bloques*BLOCK);
	
	suma <<< bloques, BLOCK >>>(dev_vector1, dev_vector2, dev_resultado, n);

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
	printf("\n<pulsa [INTRO] para finalizar>\n");
	getchar();
	return 0;
}
///////////////////////////////////////////////////////////////////////////
// HOST: funcion llamada desde el host y ejecutada en el host
__host__ void propiedades_Device(int deviceID)
{
	cudaDeviceProp deviceProp;
	cudaGetDeviceProperties(&deviceProp, deviceID);
	// calculo del numero de cores (SP)
	int cudaCores = 0;
	int SM = deviceProp.multiProcessorCount;
	int major = deviceProp.major;
	int minor = deviceProp.minor;
	switch (major)
	{
	case 1:
		//TESLA
		cudaCores = 8;
		break;
	case 2:
		//FERMI
		if (minor == 0)
			cudaCores = 32;
		else
			cudaCores = 48;
		break;
	case 3:
		//KEPLER
		cudaCores = 192;
		break;
	case 5:
		//MAXWELL
		cudaCores = 128;
		break;
	case 6:
		//PASCAL
		cudaCores = 64;
		break;
	case 7:
		//VOLTA (7.0) TURING (7.5)
		cudaCores = 64;
		break;
	case 8:
		//AMPERE
		cudaCores = 64;
		break;
	default:
		//ARQUITECTURA DESCONOCIDA
		cudaCores = 0;
		printf("!!!!!dispositivo desconocido!!!!!\n");
	}
	// presentacion de propiedades
	printf("***************************************************\n");
	printf("DEVICE %d: %s\n", deviceID, deviceProp.name);
	printf("***************************************************\n");
	printf("> Capacidad de Computo            \t: %d.%d\n", major, minor);
	printf("> No. de MultiProcesadores        \t: %d \n", SM);
	printf("> No. de CUDA Cores (%dx%d)       \t: %d \n", cudaCores, SM, cudaCores*SM);
	printf("> No. maximo de Hilos (por bloque)\t: %d\n", deviceProp.maxThreadsPerBlock);
	printf(" [eje x -> %d]\n [eje y -> %d]\n [eje z -> %d]\n", deviceProp.maxThreadsDim[0], deviceProp.maxThreadsDim[1], deviceProp.maxThreadsDim[2]);
	printf("> No. maximo de Bloques (por eje):\n");
	printf(" [eje x -> %d]\n [eje y -> %d]\n [eje z -> %d]\n", deviceProp.maxGridSize[0], deviceProp.maxGridSize[1], deviceProp.maxGridSize[2]);
	printf("***************************************************\n");
}

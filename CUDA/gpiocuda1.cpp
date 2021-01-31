// inclusión de librerias
#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>
#include <chrono> 
#include <thread>
#include <signal.h>
#include <JetsonGPIO.h>


int output_pin= 12;
int output_pin2=18;

bool end = false;
inline void delay (int s)
{
	this_thread::sleep_for(chrono::seconds(s));
}

void signalHandler(int s)
{
	end=true;

}

__global__void mult(int *vector_1, int *vector_2, int *verctor_mul, int n)
{
	// identificador de hilos
	int myID= threadIdx.x;
	//generación de los vectores
	vector_2[myID]=myID;
	vector_1[myID]=myID;
	// resultado 
	verctor_mul[myID]=vector_1[myID]*vector_2[myID];
}

int main(int arc, char** argv)
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
		hst_vector1[i] = 0;
		hst_vector2[i] = 0;
	}
	
	// LANZAMIENTO DEL KERNEL
	mult <<< 1, n >>>(dev_vector1, dev_vector2, dev_resultado, n);
	
	// recogida de datos desde el device
	cudaMemcpy(hst_vector1, dev_vector1, n * sizeof(int), cudaMemcpyDeviceToHost);
	cudaMemcpy(hst_vector2, dev_vector2, n * sizeof(int), cudaMemcpyDeviceToHost);
	cudaMemcpy(hst_resultado, dev_resultado, n * sizeof(int), cudaMemcpyDeviceToHost);
	
	signal(SIGINT,signalHandler);
	GPIO::setup(output_pin,GPIO::OUT,GPIO::LOW);
	GPIO::setup(output_pin2,GPIO::OUT,GPIO::LOW);
	
	


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
	
	while(!end)
	{
		if(hst_resultado[3]==4){
		output_pin=GPIO::HIGH;
		output_pin2=GPIO::LOW;
	
		}
		
		else{
		output_pin2=GPIO::HIGH;
		output_pin1=GPIO::LOW;
		
		}
		
	}

}
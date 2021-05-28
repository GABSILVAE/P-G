#include <stdio.h>
#include <cuda_runtime.h>
#define columnas 3
#define filas 3
__global__ void add(int *a, int *b, int *c) {

 int x = blockIdx.x * blockDim.x + threadIdx.x;
 int y = blockIdx.y * blockDim.y + threadIdx.y;
 int i = (columnas * y) + x;

 c[i] = a[i] + b[i];
}

int main() {
 int cont = 0;
 int i, j;
 // matrices en host
 int a[filas][columnas], b[filas][columnas], c[filas][columnas];

 // matrices en GPGPU
 int *dev_a, *dev_b, *dev_c;

 cudaMalloc((void **) &dev_a, filas * columnas * sizeof(int));
 cudaMalloc((void **) &dev_b, filas * columnas * sizeof(int));
 cudaMalloc((void **) &dev_c, filas * columnas * sizeof(int));

 /* inicializando variables con datos foo*/
 for (i = 0; i < filas; i++) {
  cont = 0;
  for (j = 0; j < columnas; j++) {
   a[i][j] = 2;
   b[i][j] = 5;
   cont++;
  }
 }
 cudaMemcpy(dev_a, a, filas * columnas * sizeof(int),cudaMemcpyHostToDevice);
 cudaMemcpy(dev_b, b, filas * columnas * sizeof(int),cudaMemcpyHostToDevice);

 // definiendo grid
 dim3 grid(columnas, filas);

 // grid del tamaño de la matriz, con un thread por bloque
 add<<<grid, 2>>>(dev_a, dev_b, dev_c);

 cudaMemcpy(c, dev_c, filas * columnas * sizeof(int), cudaMemcpyDeviceToHost);

 // imprimiendo
 for (int y = 0; y < filas; y++)
   {
  for (int x = 0; x < columnas; x++) {
   printf("[%d][%d]=%d ", y, x, c[y][x]);
  }
  printf("\n");
 }
 return 0;
}

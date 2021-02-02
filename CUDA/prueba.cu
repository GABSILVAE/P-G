#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>
__host__ int pow (int arg , int exp){
	
	int i;
	int res=0;	
	for (i=0; i<exp; i++){
		
		res*= arg;
		}
		
	return res;
	
	}


int main(int *argc, char** argv[]) {
	int res=0;
	rs = pow (2,3);
	printf ("el resultado es %d",rs );
	 
	return 0;
}
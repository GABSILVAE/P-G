#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>
__host__ char pow (int arg , int exp){
	
	int i;
	int res=0;	
	for (i=0; i<exp; i++){
		
		res*= arg;
		}
		
	return res;
	
	}


int main(int *argc, char** argv[]) {

	int res=0;
	res = pow (2,3);
	printf ("el resultado es %d",res );
	 
	return 0;
}
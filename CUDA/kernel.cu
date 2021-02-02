#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>

using namespace std;

__host__ void writeFile(char *fileName, char line[]) {
	FILE* file;
	file = fopen(fileName, "w");

	fputs(line, file);

	fclose(file);
}

int main(int *argc, char** argv[]) {
	printf("Script for writting a line to a txt file");

	char line[255] = "Helo world from Host";

	writeFile("test.txt", line);

	return 0;
}
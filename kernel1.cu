#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <poll.h>

using namespace std;

#define SYSFS_GPIO_DIR "/sys/class/gpio"
#define POLL_TIMEOUT (3 * 1000) /* 3 seconds */
#define MAX_BUF 64

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

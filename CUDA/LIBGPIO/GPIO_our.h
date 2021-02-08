#include <iostream>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <poll.h>
#include <chrono> 
#include <thread>

#include <cuda_runtime.h>
#define SYSFS_GPIO_DIR "/sys/class/gpio"
#define MAX_BUF 64

__host__ int gpio_export(unsigned int gpio);
__host__ int gpio_unexport(unsigned int gpio);
__host__ int gpio_set_dir(unsigned int gpio, unsigned int out_flag);
__host__ int gpio_set_value(unsigned int gpio, unsigned int value);
__host__ int gpio_get_value(unsigned int gpio, unsigned int *value);
__host__ int gpio_set_edge(unsigned int gpio, char *edge);
__host__ int gpio_fd_open(unsigned int gpio);
__host__ int gpio_fd_close(int fd);
__host__ void delay(int s);
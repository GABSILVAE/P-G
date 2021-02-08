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

#define SYSFS_GPIO_DIR "/sys/class/gpio"
#define MAX_BUF 64
#define unsigned int Key_deco[41]={0,0,0,0,0,0,0,216,0,0,0,50,79,14,0,194,232,0,15,16,0,17,13,18,19,0,20,0,0,149,0,200,168,38,0,76,51,12,77,0,78};

__host__ int gpio_export(unsigned int gpio);
__host__ int gpio_unexport(unsigned int gpio);
__host__ int gpio_set_dir(unsigned int gpio, unsigned int out_flag);
__host__ int gpio_set_value(unsigned int gpio, unsigned int value);
__host__ int gpio_get_value(unsigned int gpio, unsigned int *value);
__host__ int gpio_set_edge(unsigned int gpio, char *edge);
__host__ int gpio_fd_open(unsigned int gpio);
__host__ int gpio_fd_close(int fd);
__host__ inline void delay(int s);
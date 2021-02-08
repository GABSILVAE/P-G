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
using namespace std;

#define SYSFS_GPIO_DIR "/sys/class/gpio"
#define MAX_BUF 64

#define unsigned int Key_deco[41]={0,0,0,0,0,0,0,216,0,0,0,50,79,14,0,194,232,0,15,16,0,17,13,18,19,0,20,0,0,149,0,200,168,38,0,76,51,12,77,0,78};
unsigned int gpiod, pin;

__host__ int gpio_export(unsigned int gpio){
	int fd, len;
	char buf[MAX_BUF];
 
	fd = open(SYSFS_GPIO_DIR "/export", O_WRONLY);
	if (fd < 0) {
		perror("gpio/export");
		return fd;
	}
 
	len = snprintf(buf, sizeof(buf), "%d", gpio);
	write(fd, buf, len);
	close(fd);
 
	return 0;
}

__host__ int gpio_unexport(unsigned int gpio){
	int fd, len;
	char buf[MAX_BUF];
 
	fd = open(SYSFS_GPIO_DIR "/unexport", O_WRONLY);
	if (fd < 0) {
		perror("gpio/export");
		return fd;
	}
 
	len = snprintf(buf, sizeof(buf), "%d", gpio);
	write(fd, buf, len);
	close(fd);
	return 0;
}

__host__ int gpio_set_dir(unsigned int gpio, unsigned int out_flag){
	int fd, len;
	char buf[MAX_BUF];
 
	len = snprintf(buf, sizeof(buf), SYSFS_GPIO_DIR  "/gpio%d/direction", gpio);
 
	fd = open(buf, O_WRONLY);
	if (fd < 0) {
		perror("gpio/direction");
		return fd;
	}
 
	if (out_flag)
		write(fd, "out", 4);
	else
		write(fd, "in", 3);
 
	close(fd);
	return 0;
}

__host__ int gpio_set_value(unsigned int gpio, unsigned int value){
	int fd, len;
	char buf[MAX_BUF];
 
	len = snprintf(buf, sizeof(buf), SYSFS_GPIO_DIR "/gpio%d/value", gpio);
 
	fd = open(buf, O_WRONLY);
	if (fd < 0) {
		perror("gpio/set-value");
		return fd;
	}
 
	if (value)
		write(fd, "1", 2);
	else
		write(fd, "0", 2);
 
	close(fd);
	return 0;
}

__host__ int gpio_get_value(unsigned int gpio, unsigned int *value){
	int fd, len;
	char buf[MAX_BUF];
	char ch;

	len = snprintf(buf, sizeof(buf), SYSFS_GPIO_DIR "/gpio%d/value", gpio);
 
	fd = open(buf, O_RDONLY);
	if (fd < 0) {
		perror("gpio/get-value");
		return fd;
	}
 
	read(fd, &ch, 1);

	if (ch != '0') {
		*value = 1;
	} else {
		*value = 0;
	}
 
	close(fd);
	return 0;
}

__host__ int gpio_set_edge(unsigned int gpio, char *edge){
	int fd, len;
	char buf[MAX_BUF];

	len = snprintf(buf, sizeof(buf), SYSFS_GPIO_DIR "/gpio%d/edge", gpio);
 
	fd = open(buf, O_WRONLY);
	if (fd < 0) {
		perror("gpio/set-edge");
		return fd;
	}
 
	write(fd, edge, strlen(edge) + 1); 
	close(fd);
	return 0;
}

__host__ int gpio_fd_open(unsigned int gpio){
	int fd, len;
	char buf[MAX_BUF];

	len = snprintf(buf, sizeof(buf), SYSFS_GPIO_DIR "/gpio%d/value", gpio);
 
	fd = open(buf, O_RDONLY | O_NONBLOCK );
	if (fd < 0) {
		perror("gpio/fd_open");
	}
	return fd;
}

__host__ int gpio_fd_close(int fd){
	return close(fd);
}

__host__ inline void delay(int s){
	this_thread::sleep_for(chrono::seconds(s));
}

int main(int *argc, char** argv[]){	
	cout << "		INICIO		" << "\n";
	pin = 13;
	gpiod = Key_deco[pin];

	gpio_export(gpiod);
	delay(5);
	gpio_set_dir(gpiod,1);
	delay(5);

	while(1){
		cout << "VALOR = " << gpiod << "\n"; 
		cout << "Prendido" << "\n";
		gpio_set_value(gpiod,1);
		delay(1);
		cout << "Apagado" << "\n";
		gpio_set_value(gpiod,0);
		delay(1);
	}
	return 0;
}
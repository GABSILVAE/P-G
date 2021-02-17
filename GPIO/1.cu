#include <linux/module.h>   
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/gpio.h>
#include <linux/interrupt.h>

#define LED 27
#define BUTTON 23
#define MY_GPIO_INT_NAME "my_button_int"
#define MY_DEV_NAME "my_device"

int main(int *argc, char** argv[]){	
	// -- setup the led gpio as output
	printk("module: button interrupt example.\n");
	if(gpio_is_valid(LED) < 0) return -1;
	if(gpio_request(LED, "LED") < 0) return -1;
	gpio_direction_output(LED, 0 );

	// -- setup the button gpio as input and request irq
	if(gpio_request(BUTTON,"BUTTON") < 0) return -1;
	if(gpio_is_valid(BUTTON) < 0) return -1;
	if( (button_irq = gpio_to_irq(BUTTON)) < 0 )  return -1;
	if( request_irq( button_irq, button_isr ,IRQF_TRIGGER_RISING, MY_GPIO_INT_NAME, MY_DEV_NAME)) return -1;
	return 0;
}
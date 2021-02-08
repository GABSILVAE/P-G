#include "GPIO_our.h"

unsigned int gpiod, pin;

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
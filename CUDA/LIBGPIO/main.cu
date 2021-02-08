#include "GPIO_our.h"

using namespace std;
unsigned int gpiod, pin;
unsigned int Key_deco[41]={0,0,0,0,0,0,0,216,0,0,0,50,79,14,0,194,232,0,15,16,0,17,13,18,19,0,20,0,0,149,0,200,168,38,0,76,51,12,77,0,78};

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
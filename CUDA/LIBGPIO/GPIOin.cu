#include "GPIOlib.cu"

using namespace std;
unsigned int in,out,pin_in,pin_out,valor;
unsigned int Key_deco[41]={0,0,0,0,0,0,0,216,0,0,0,50,79,14,0,194,232,0,15,16,0,17,13,18,19,0,20,0,0,149,0,200,168,38,0,76,51,12,77,0,78};

int main(int *argc,char**argv[]){
	
	pin_in=13;
	pin_out=7;
	in=Key_deco[pin_in];
	out = Key_deco[pin_out];
	
	gpio_export(in);
	delay(1);	
	gpio_export(out);
	delay(1);
	
	gpio_set_dir(in,0);
	delay(1);
	gpio_set_dir(out,1);
	delay(1);
	
	while(1){
		gpio_get_value(in,valor);
		
		if(valor==1){
			cout << "switch encendido"<<"\n";
			gpio_set_value(out,value);
		}
		else{
			cout << "switch apagado"<<"\n";
			gpio_set_value(out,value);
		}
	}
	return 0;
}
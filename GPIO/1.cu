#include <linux/gpio.h>
#include <iostream>

int main(int *argc, char** argv[]){	
    const bool is17Valid = !!gpio_is_valid(17);
    if (is17Valid)
    {
        std::cout << "17 is valid!" << std::endl;
    }
    else
    {
        std::cout << "17 is *not* valid!" << std::endl;
    }

    return 0;
}
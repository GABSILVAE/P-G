#include <stdio.h>
int main()
{
	int a;
	int b;
	int *p;
	a=13;
	p=&a;
	int **q =&p;
	int ***r=&q;
	printf("%d\n",a);
	printf("la salida es %d\n", **q);
	printf("la salida es %d\n", ***r);

}

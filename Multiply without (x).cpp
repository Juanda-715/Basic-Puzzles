#include<iostream>
using namespace std;
double multiplicar(double, double);
int main()
{
	double a, b, res;
	cout << "Ingrese dos numeros para multiplicar: " << endl;
	cout << "1: ";
	cin >> a;
	cout << "2: ";
	cin >> b;
	res = multiplicar(a, b);
	cout << "El restultado de la multiplicacion entre " << a << " y " << b << " es: " << res << endl;
}
double multiplicar(double a, double b)
{
	double resultado = 0, z;
	if (a < 0)
	{
		z = a;
		a = b;
		b = z;
	}
	if (a < 0 && b < 0)
	{
		a = a - (a + a);
		b = b - (b + b);
		for (int c = 1; c <= a; c++)
		{
			resultado += b;
		}
	}
	else
	{
		for (int c = 1; c <= a; c++)
		{
			resultado += b;
		}
	}

		return resultado;
}
// Buena le rat
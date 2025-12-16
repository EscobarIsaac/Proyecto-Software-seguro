#include <iostream>
#include "entrenar_modelo.h"
#include "usar_modelo.h"

using namespace mlpack;
using namespace arma;
using namespace std;

void mostrar_menu() {
	system("cls");
    cout << "\n=== SISTEMA DE DETECCION DE VULNERABILIDADES ===\n";
    cout << "1. Entrenar modelo\n";
    cout << "2. Usar modelo (predecir)\n";
    cout << "3. Salir\n";
    cout << "Seleccione una opcion: ";
}

int main()
{
    int opcion;
    
    do {
        mostrar_menu();
        cin >> opcion;
        
        switch(opcion) {
            case 1:
            	system("cls");
                cout << "\nEntrenando modelo...\n";
                try {
                    entrenar_modelo_mineriadatos();
                } catch(const exception& e) {
                    cerr << "Error al entrenar el modelo: " << e.what() << endl;
                }
                system("pause");
                break;
                
            case 2:
            	system("cls");
                cout << "\nUsando modelo para prediccion...\n";
                try {
                    usar_modelo_mineriadatos();
                } catch(const exception& e) {
                    cerr << "Error al usar el modelo: " << e.what() << endl;
                }
                system("pause");
                break;
                
            case 3:
            	system("cls");
                cout << "\nSaliendo del programa...\n";
                break;
                
            default:
                cout << "\nOpción invalida. Por favor seleccione 1, 2 o 3.\n";
                system("pause");
        }
        
    } while(opcion != 3);
    
    return 0;
}

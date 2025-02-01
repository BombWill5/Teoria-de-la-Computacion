import random
import time

import buscador
import automatapila
import backusNaur
import MT

programas = {
    "buscador": buscador.main,
    "automatapila": automatapila.main,
    "backusNaur": backusNaur.main,
    "MT": MT.main,
}

def ejecutar_programa_aleatorio():
    programa_seleccionado = random.choice(list(programas.keys()))
    print(f"\nEjecutando: {programa_seleccionado}")
    
    # Ejecutar el programa
    programas[programa_seleccionado]()

def ejecutar_programa_manual():
    print("\nProgramas disponibles:")
    for i, programa in enumerate(programas.keys(), 1):
        print(f"{i}. {programa}")
    print(f"{len(programas) + 1}. Salir")

    # Solicitar al usuario seleccionar un programa
    while True:
        try:
            opcion = int(input("Seleccione un programa por su número: "))
            if 1 <= opcion <= len(programas):
                programa_seleccionado = list(programas.keys())[opcion - 1]
                print(f"\nEjecutando: {programa_seleccionado}")
                programas[programa_seleccionado]()
                break
            elif opcion == len(programas) + 1:
                print("Saliendo del menú manual...")
                break
            else:
                print("Opción inválida. Intente nuevamente.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")

def main():
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Ejecutar 10 programas aleatorios automáticamente")
        print("2. Elegir un programa para ejecutar manualmente")
        print("3. Salir")
        
        try:
            opcion = int(input("Seleccione una opción: "))
            if opcion == 1:
                iteraciones = 10
                print("\nEjecutando 10 programas de forma automática...")
                for _ in range(iteraciones):
                    ejecutar_programa_aleatorio()
                    time.sleep(random.uniform(1, 3))
            elif opcion == 2:
                ejecutar_programa_manual()
            elif opcion == 3:
                print("Saliendo del programa...")
                break
            else:
                print("Opción inválida. Intente nuevamente.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")

if __name__ == "__main__":
    main()

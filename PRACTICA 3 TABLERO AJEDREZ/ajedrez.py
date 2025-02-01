import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import networkx as nx
import time

class AFND:
    def __init__(self, estado_inicial, estado_final):
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final
        self.alfabeto = {'r', 'b'}
        self.transiciones = {1: {'r': [2, 6], 'b': [7]},
                             2: {'r': [6, 8], 'b': [1, 3, 7]},
                             3: {'r': [2, 4, 8], 'b': [7, 9]},
                             4: {'r': [8, 10], 'b': [3, 5, 9]},
                             5: {'r': [4, 10], 'b': [9]},
                             6: {'r': [2, 12], 'b': [1, 7, 11]},
                             7: {'r': [2, 6, 8, 12], 'b': [1, 3, 11, 13]},
                             8: {'r': [2, 4, 12, 14], 'b': [3, 7, 9, 13]},
                             9: {'r': [4, 8, 10, 14], 'b': [3, 5, 13, 15]},
                             10: {'r': [4, 14], 'b': [5, 9, 15]},
                             11: {'r': [6, 12, 16], 'b': [7, 17]},
                             12: {'r': [6, 8, 16, 18], 'b': [7, 11, 13, 17]},
                             13: {'r': [8, 12, 14, 18], 'b': [7, 9, 17, 19]},
                             14: {'r': [8, 10, 18, 20], 'b': [9, 13, 15, 19]},
                             15: {'r': [10, 14, 20], 'b': [9, 19]},
                             16: {'r': [12, 22], 'b': [11, 17, 21]},
                             17: {'r': [12, 16, 18, 22], 'b': [11, 13, 21, 23]},
                             18: {'r': [12, 14, 22, 24], 'b': [13, 17, 19, 23]},
                             19: {'r': [14, 18, 20, 24], 'b': [13, 15, 23, 25]},
                             20: {'r': [14, 24], 'b': [15, 19, 25]},
                             21: {'r': [16, 22], 'b': [17]},
                             22: {'r': [16, 18], 'b': [17, 21, 23]},
                             23: {'r': [18, 22, 24], 'b': [17, 19]},
                             24: {'r': [18, 20], 'b': [19, 23, 25]},
                             25: {'r': [20, 24], 'b': [19]}}

    def procesar(self, cadena, jugador):
        pila = [(self.estado_inicial, cadena, [self.estado_inicial], [])]

        resultado = False

        while pila:
            estado_actual, cadena_restante, ruta, transiciones = pila.pop()

            if len(cadena_restante) == 0:
                with open(f"Rutas{jugador}.txt", "a") as archivo:
                    archivo.write(" ".join(map(str, ruta)) + "\n")
                    archivo.write(" ".join(transiciones) + "\n")
                if estado_actual == self.estado_final:
                    resultado = True
                    with open(f"Ganadoras{jugador}.txt", "a") as archivo:
                        archivo.write(" ".join(map(str, ruta)) + "\n")
                        archivo.write(" ".join(transiciones) + "\n")
                else:
                    with open(f"Perdedoras{jugador}.txt", "a") as archivo:
                        archivo.write(" ".join(map(str, ruta)) + "\n")
                        archivo.write(" ".join(transiciones) + "\n")
                continue

            simbolo = cadena_restante[0]
            estados_siguientes = self.transiciones.get(estado_actual, {}).get(simbolo, [])
            if estados_siguientes == []:
                print(f"Error: No hay transiciones disponibles desde el estado {estado_actual} con el símbolo '{simbolo}'")
                exit()
            for estado_sig in estados_siguientes:
                pila.append((estado_sig, cadena_restante[1:], ruta + [estado_sig], transiciones + [simbolo]))

        return resultado

def inicializar_tablero():
    tablero = []
    for row in range(5):
        for col in range(5):
            estado = row * 5 + col + 1
            if estado == 1:
                tablero.append(2)  # Azul para el jugador 1
            elif estado == 5:
                tablero.append(3)  # Café para el jugador 2
            elif (row + col) % 2 == 0:
                tablero.append(0)  # Negro
            else:
                tablero.append(1)  # Rojo
    return tablero

def actualizar_tablero(tablero, estado_actual, estado_previo, jugador, ax):
    # Restaurar la casilla anterior al color original
    if estado_previo is not None:
        row_prev = (estado_previo - 1) // 5
        col_prev = (estado_previo - 1) % 5
        if (row_prev + col_prev) % 2 == 0:
            tablero[estado_previo - 1] = 0  # Negro
        else:
            tablero[estado_previo - 1] = 1  # Rojo

    # Actualizar la casilla actual con el color del jugador
    if jugador == 1:
        tablero[estado_actual - 1] = 2  # Azul para el jugador 1
    elif jugador == 2:
        tablero[estado_actual - 1] = 3  # Café para el jugador 2

    mostrar_tablero(tablero, ax)

def mostrar_tablero(tablero, ax):
    tablero_2d = np.array(tablero).reshape((5, 5))

    ax.clear()
    cmap = mcolors.ListedColormap(['black', 'red', 'blue', 'brown'])
    ax.imshow(tablero_2d, cmap=cmap, extent=[0, 5, 0, 5])

    ax.set_xticks(np.arange(6))
    ax.set_yticks(np.arange(6))
    ax.grid(True, which='both')

    for i in range(5):
        for j in range(5):
            estado = i * 5 + j + 1
            ax.text(j + 0.5, 4 - i + 0.5, str(estado), ha='center', va='center', color='white', fontsize=12)

    ax.set_xticks([])
    ax.set_yticks([])

    plt.draw()
    plt.pause(1)

def juego(ruta1, ruta2, primero):
    with open(ruta1, "r") as Ganadoras1:
        lineas1 = Ganadoras1.readlines()
    with open(ruta2, "r") as Ganadoras2:
        lineas2 = Ganadoras2.readlines()

    # Filtrar las líneas que contienen los estados (solo las líneas impares, ya que las pares contienen los símbolos)
    jugadas1 = [lineas1[i] for i in range(0, len(lineas1), 2)]  # Solo las líneas impares (0, 2, 4, ...)
    jugadas2 = [lineas2[i] for i in range(0, len(lineas2), 2)]  # Solo las líneas impares

    if len(jugadas1) >= 1:
        if len(jugadas2) >= 1:
            jugadaActual1 = [int(estado) for estado in jugadas1[0].strip().split()]
            jugadaActual2 = [int(estado) for estado in jugadas2[0].strip().split()]
        else:
            print("El jugador 2 no tiene jugadas ganadoras. Jugador 1 gana por default.")
            exit()
    else:
        if len(jugadas2) >= 1:
            print("El jugador 1 no tiene jugadas ganadoras. Jugador 2 gana por default.")
            exit()
        else:
            print("Ningún jugador tiene jugadas ganadoras. Ambos pierden.")
            exit()

    contadorEstado1 = contadorEstado2 = 0
    contadorJugada1 = contadorJugada2 = 0
    topeContador = len(jugadaActual1) - 1  # Todas las jugadas tienen la misma longitud

    # Inicializar el tablero con los colores predeterminados de los jugadores 1 y 2
    tablero = inicializar_tablero()
    estadoActual1 = jugadaActual1[0]
    estadoActual2 = jugadaActual2[0]
    estadoPrevio1 = estadoPrevio2 = None

    # Crear la figura para graficar
    fig, ax = plt.subplots()
    mostrar_tablero(tablero, ax)

    # Esperar 1 segundo antes de empezar
    time.sleep(1)

    turno = primero  # 1 o 2

    while True:
        if turno == 1:
            # Movimiento del jugador 1
            if contadorEstado1 + 1 <= topeContador:
                siguienteEstado1 = jugadaActual1[contadorEstado1 + 1]
                if siguienteEstado1 != estadoActual2:
                    estadoPrevio1 = estadoActual1
                    estadoActual1 = siguienteEstado1
                    contadorEstado1 += 1
                    actualizar_tablero(tablero, estadoActual1, estadoPrevio1, 1, ax)
                    print(f"Jug1: {estadoActual1}")
                    if contadorEstado1 == topeContador:
                        print("Jugador 1 Gana.")
                        break
                    turno = 2  # Cambiar el turno al jugador 2
                else:
                    # Intentar reconfigurar la ruta
                    ruta_encontrada = False
                    for i in range(contadorJugada1 + 1, len(jugadas1)):
                        posible_jugada = [int(estado) for estado in jugadas1[i].strip().split()]
                        if posible_jugada[contadorEstado1] == estadoActual1 and posible_jugada[contadorEstado1 + 1] != estadoActual2:
                            jugadaActual1 = posible_jugada
                            contadorJugada1 = i
                            siguienteEstado1 = jugadaActual1[contadorEstado1 + 1]
                            estadoPrevio1 = estadoActual1
                            estadoActual1 = siguienteEstado1
                            contadorEstado1 += 1
                            actualizar_tablero(tablero, estadoActual1, estadoPrevio1, 1, ax)
                            print(f"Jugador 1 reconfiguró su ruta a: {jugadaActual1}")
                            print(f"Jug1: {estadoActual1}")
                            if contadorEstado1 == topeContador:
                                print("Jugador 1 Gana.")
                                plt.show()
                                return
                            ruta_encontrada = True
                            turno = 2
                            break
                    if not ruta_encontrada:
                        print(f"Jugador 1 no puede moverse en el turno {contadorEstado1 + 1}. Cede el turno.")
                        turno = 2  # Ceder el turno al jugador 2
            else:
                print("Jugador 1 no tiene más movimientos.")
                turno = 2

        else:
            # Movimiento del jugador 2
            if contadorEstado2 + 1 <= topeContador:
                siguienteEstado2 = jugadaActual2[contadorEstado2 + 1]
                if siguienteEstado2 != estadoActual1:
                    estadoPrevio2 = estadoActual2
                    estadoActual2 = siguienteEstado2
                    contadorEstado2 += 1
                    actualizar_tablero(tablero, estadoActual2, estadoPrevio2, 2, ax)
                    print(f"Jug2: {estadoActual2}")
                    if contadorEstado2 == topeContador:
                        print("Jugador 2 Gana.")
                        break
                    turno = 1  # Cambiar el turno al jugador 1
                else:
                    # Intentar reconfigurar la ruta
                    ruta_encontrada = False
                    for i in range(contadorJugada2 + 1, len(jugadas2)):
                        posible_jugada = [int(estado) for estado in jugadas2[i].strip().split()]
                        if posible_jugada[contadorEstado2] == estadoActual2 and posible_jugada[contadorEstado2 + 1] != estadoActual1:
                            jugadaActual2 = posible_jugada
                            contadorJugada2 = i
                            siguienteEstado2 = jugadaActual2[contadorEstado2 + 1]
                            estadoPrevio2 = estadoActual2
                            estadoActual2 = siguienteEstado2
                            contadorEstado2 += 1
                            actualizar_tablero(tablero, estadoActual2, estadoPrevio2, 2, ax)
                            print(f"Jugador 2 reconfiguró su ruta a: {jugadaActual2}")
                            print(f"Jug2: {estadoActual2}")
                            if contadorEstado2 == topeContador:
                                print("Jugador 2 Gana.")
                                plt.show()
                                return
                            ruta_encontrada = True
                            turno = 1
                            break
                    if not ruta_encontrada:
                        print(f"Jugador 2 no puede moverse en el turno {contadorEstado2 + 1}. Cede el turno.")
                        turno = 1  # Ceder el turno al jugador 1
            else:
                print("Jugador 2 no tiene más movimientos.")
                turno = 1


    # Mantener la ventana abierta al finalizar el juego
    plt.show()

def vaciarArchivos():
    with open("Rutas1.txt", "w") as archivo:
        archivo.write("")
    with open("Ganadoras1.txt", "w") as archivo:
        archivo.write("")
    with open("Perdedoras1.txt", "w") as archivo:
        archivo.write("")
    with open("Rutas2.txt", "w") as archivo:
        archivo.write("")
    with open("Ganadoras2.txt", "w") as archivo:
        archivo.write("")
    with open("Perdedoras2.txt", "w") as archivo:
        archivo.write("")

def generarCadena(tamañoCadena):
    cadena = ""
    for i in range(tamañoCadena - 1):
        cadena += random.choice(['r', 'b'])
    cadena += 'b'
    return cadena

def graficar_rutas(archivo_rutas, jugador):
    with open(archivo_rutas, "r") as archivo:
        lineas = archivo.readlines()

    # Crear un grafo dirigido
    Grafo = nx.DiGraph()

    # Procesar las rutas y sus transiciones (estados en una línea, símbolos en la siguiente)
    for i in range(0, len(lineas), 2):
        estados = list(map(int, lineas[i].strip().split()))
        transiciones = lineas[i+1].strip().split()

        # Agregar los nodos y arcos al grafo con las etiquetas correspondientes
        for j in range(len(estados) - 1):
            Grafo.add_edge(estados[j], estados[j + 1], label=transiciones[j])

    # Obtener posiciones arbitrarias de los nodos usando un layout de resorte
    pos = nx.spring_layout(Grafo)

    # Dibujar el grafo
    plt.figure(figsize=(8, 8))
    nx.draw(Grafo, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=10, font_weight='bold', arrowstyle='->', arrowsize=15)

    # Dibujar las etiquetas de los arcos (las transiciones 'r' o 'b')
    edge_labels = nx.get_edge_attributes(Grafo, 'label')
    nx.draw_networkx_edge_labels(Grafo, pos, edge_labels=edge_labels, font_color='red')

    # Añadir título
    plt.title(f"Caminos del Jugador {jugador}")
    plt.show()

def mostrar_caminos():
    graficar_rutas("Ganadoras1.txt", 1)
    graficar_rutas("Ganadoras2.txt", 2)
    # Mostrar ambas gráficas juntas
    plt.show()

def main():
    vaciarArchivos()
    print("Bienvenido al juego del Tablero")
    print("1. Modo Automático\n2. Modo Manual")
    while True:
        try:
            opcion = int(input("Seleccione una opción (1 o 2): "))
            if opcion in [1, 2]:
                break
            else:
                print("Por favor, ingrese 1 o 2.")
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número entero.")

    if opcion == 1:
        rey1 = AFND(1, 25)
        rey2 = AFND(5, 21)
        tamañoCadena = random.randint(5, 100)
        cadena1 = generarCadena(tamañoCadena)
        cadena2 = generarCadena(tamañoCadena)

        print(f"Cadena para el jugador 1: {cadena1}")
        print(f"Cadena para el jugador 2: {cadena2}")
        
        rey1.procesar(cadena1, 1)
        rey2.procesar(cadena2, 2)
        primero = random.choice([1, 2])

        print(f"Empieza el jugador {primero}")
        juego("Ganadoras1.txt", "Ganadoras2.txt", primero)
        mostrar_caminos()
    else:
        rey1 = AFND(1, 25)
        rey2 = AFND(5, 21)
        while True:
            cadena1 = input("Ingrese la cadena con la que jugará el jugador 1:\n")
            if len(cadena1) < 5 or len(cadena1) > 100:
                print("Por favor, ingrese una cadena de entre 5 y 100 caracteres de longitud.")
            else:
                break
        while True:
            cadena2 = input("Ingrese la cadena con la que jugará el jugador 2:\n")
            if len(cadena2) == len(cadena1):
                break
            else:
                print(f"Por favor, ingrese una cadena de la misma longitud. La longitud de la primera cadena es: {len(cadena1)} ")
        
        print(f"Cadena para el jugador 1: {cadena1}")
        print(f"Cadena para el jugador 2: {cadena2}")

        if cadena1[-1] == 'r':
            if cadena2[-1] == 'r':
                print("Ningún jugador tiene jugadas ganadoras. Ambos pierden.")
                exit()
            else:
                print("El jugador 1 no tiene jugadas ganadoras. Jugador 2 gana por default.")
                exit()
        else:
            if cadena2[-1] == 'r':
                print("El jugador 2 no tiene jugadas ganadoras. Jugador 1 gana por default.")
                exit()

        rey1.procesar(cadena1, 1)
        rey2.procesar(cadena2, 2)
        primero = random.choice([1, 2])

        print(f"Empieza el jugador {primero}")
        juego("Ganadoras1.txt", "Ganadoras2.txt", primero)
        mostrar_caminos()

if __name__ == "__main__":
    main()

import random
import tkinter as tk  # Importa Tkinter para la animación gráfica

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.next = None

class Pila:
    def __init__(self):
        self.top = None

    def isEmpty(self):
        return self.top is None

    def push(self, dato):
        nuevoNodo = Nodo(dato)
        nuevoNodo.next = self.top
        self.top = nuevoNodo

    def pop(self):
        if self.isEmpty():
            return None
        else:
            dato = self.top.dato
            self.top = self.top.next
            return dato

    def mostrarPila(self):
        """ Devuelve la pila completa como una lista de elementos desde el tope al fondo. """
        elementos = []
        actual = self.top
        while actual:
            elementos.append(actual.dato)
            actual = actual.next
        return elementos  # Orden de tope a fondo

    def peek(self):
        return None if self.isEmpty() else self.top.dato

class AutomataAnimado(tk.Tk):
    def __init__(self, cadena, transiciones):
        super().__init__()
        self.cadena = cadena
        self.transiciones = transiciones
        self.title("Animación del Autómata de Pila")
        self.geometry("300x400")
        self.canvas = tk.Canvas(self, width=300, height=400, bg="lightblue")
        self.canvas.pack()
        self.paso = 0
        self.dibujarTransicion()

    def dibujarTransicion(self):
        if self.paso < len(self.transiciones):
            estado, cadena_restante, pila = self.transiciones[self.paso]
            self.canvas.delete("all")

            # Dibuja el estado actual
            self.canvas.create_rectangle(100, 50, 200, 100, fill="cyan", outline="black")
            self.canvas.create_text(150, 75, text=f"Estado: {estado}", font=("Arial", 12))

            # Dibuja la cadena restante
            self.canvas.create_text(150, 150, text=f"Cadena: {cadena_restante}", font=("Arial", 12))

            # Dibuja la pila (tope arriba)
            y_pos = 200
            for elemento in pila:  # Elementos en orden tope -> fondo
                self.canvas.create_rectangle(120, y_pos, 180, y_pos + 30, fill="white", outline="black")
                self.canvas.create_text(150, y_pos + 15, text=elemento, font=("Arial", 12))
                y_pos += 35

            self.paso += 1
            self.after(1000, self.dibujarTransicion)
        else:
            self.canvas.create_text(150, 350, text="Simulación finalizada", font=("Arial", 12), fill="green")


def procesar(cadena, estadoactual):
    pilaAutomata = Pila()
    pilaAutomata.push("Z0")  # Inicializamos la pila con Z0
    indice = 0
    transiciones = [(estadoactual, cadena, pilaAutomata.mostrarPila())]

    with open("IDs.txt", "w", encoding="utf-8") as archivo:
        archivo.write(f"(q, {cadena if cadena else 'ε'}, Z0)\n")

        while indice < len(cadena):
            simbolo = cadena[indice]
            if simbolo not in ["0", "1"]:
                print("Cadena inválida.")
                transiciones.append((estadoactual, cadena[indice:], pilaAutomata.mostrarPila()))
                return False, transiciones

            if estadoactual == "q":
                if simbolo == "0":
                    pilaAutomata.push("X")
                elif simbolo == "1":
                    if pilaAutomata.peek() == "X":
                        pilaAutomata.pop()
                        estadoactual = "p"
                    else:
                        transiciones.append((estadoactual, cadena[indice:], pilaAutomata.mostrarPila()))
                        return False, transiciones

            elif estadoactual == "p":
                if simbolo == "1":
                    if pilaAutomata.peek() == "X":
                        pilaAutomata.pop()
                    else:
                        transiciones.append((estadoactual, cadena[indice:], pilaAutomata.mostrarPila()))
                        return False, transiciones
                else:
                    transiciones.append((estadoactual, cadena[indice:], pilaAutomata.mostrarPila()))
                    return False, transiciones

            indice += 1
            tripleta = (estadoactual, cadena[indice:] if indice < len(cadena) else "ε", pilaAutomata.mostrarPila())
            transiciones.append(tripleta)

            archivo.write(f"⊦({estadoactual}, {tripleta[1]}, {''.join(tripleta[2])})\n")

        # Verificación final de aceptación
        if estadoactual == "p" and pilaAutomata.peek() == "Z0":
            estadoactual = "f"
            transiciones.append((estadoactual, "ε", ["Z0"]))
            archivo.write(f"⊦(f, ε, Z0)\n")
            return True, transiciones
        else:
            transiciones.append((estadoactual, "ε", pilaAutomata.mostrarPila()))
            return False, transiciones

def main():
    print("1. Ingresar cadena\n2. Generar cadena")
    opc = input("Seleccione una opción: ")
    if opc == "1":
        cadena = input("Ingrese la cadena a analizar: ")
    elif opc == "2":
        cadena = "".join([str(random.randint(0, 1)) for _ in range(random.randint(1, 10))])
        print(f"Cadena generada: {cadena}")
    else:
        print("Opción no válida.")
        return

    # Procesar la cadena
    aceptada, transiciones = procesar(cadena, "q")

    # Mostrar si la cadena pertenece al lenguaje
    if aceptada:
        print("La cadena pertenece al lenguaje {0^n 1^n | n >= 1}.")
    else:
        print("La cadena no pertenece al lenguaje {0^n 1^n | n >= 1}.")

    # Mostrar la animación siempre si la cadena tiene <= 10 caracteres
    if len(cadena) <= 10:
        app = AutomataAnimado(cadena, transiciones)
        app.mainloop()

if __name__ == "__main__":
    main()

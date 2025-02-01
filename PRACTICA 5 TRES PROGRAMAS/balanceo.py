import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.next = None

class Pila:
    def __init__(self):
        self.top = None
        self.elementos = []  # Para visualizar la pila

    def isEmpty(self):
        return self.top is None

    def push(self, dato):
        nuevoNodo = Nodo(dato)
        nuevoNodo.next = self.top
        self.top = nuevoNodo
        self.elementos.append(dato)  # Añadir a la visualización

    def pop(self):
        if self.isEmpty():
            print("Pila vacía")
        else:
            self.top = self.top.next
            self.elementos.pop()  # Quitar de la visualización

# Pilas para cada tipo de símbolo
pilaLlaves = Pila()
pilaCorchetes = Pila()
pilaParentesis = Pila()
pilaComillas = Pila()

estadoLLaves = 'f'
estadoCorchetes = 'f'
estadoParentesis = 'f'
estadoComillas = 'f'

# Guardar cada paso para animación
frames = []

def procesar(caracter):
    global estadoLLaves, estadoCorchetes, estadoParentesis, estadoComillas

    # Llaves
    if caracter == '{' or caracter == '}':
        if estadoLLaves == 'f':
            estadoLLaves = 'q'
        if estadoLLaves == 'q':
            if caracter == '{':
                pilaLlaves.push('X')
            elif caracter == '}' and not pilaLlaves.isEmpty():
                pilaLlaves.pop()
            if pilaLlaves.isEmpty():
                estadoLLaves = 'f'

    # Corchetes
    elif caracter == '[' or caracter == ']':
        if estadoCorchetes == 'f':
            estadoCorchetes = 'q'
        if estadoCorchetes == 'q':
            if caracter == '[':
                pilaCorchetes.push('X')
            elif caracter == ']' and not pilaCorchetes.isEmpty():
                pilaCorchetes.pop()
            if pilaCorchetes.isEmpty():
                estadoCorchetes = 'f'

    # Paréntesis
    elif caracter == '(' or caracter == ')':
        if estadoParentesis == 'f':
            estadoParentesis = 'q'
        if estadoParentesis == 'q':
            if caracter == '(':
                pilaParentesis.push('X')
            elif caracter == ')' and not pilaParentesis.isEmpty():
                pilaParentesis.pop()
            if pilaParentesis.isEmpty():
                estadoParentesis = 'f'

    # Comillas
    elif caracter == '"':
        if estadoComillas == 'f':
            estadoComillas = 'q'
        if pilaComillas.isEmpty():
            pilaComillas.push('X')
        else:
            pilaComillas.pop()
        if pilaComillas.isEmpty():
            estadoComillas = 'f'

    # Capturar el estado actual de las pilas
    frames.append({
        "Llaves": len(pilaLlaves.elementos),
        "Corchetes": len(pilaCorchetes.elementos),
        "Parentesis": len(pilaParentesis.elementos),
        "Comillas": len(pilaComillas.elementos)
    })

def animar(i):
    estados = frames[i]
    ax.clear()
    ax.bar(estados.keys(), estados.values(), color='blue')
    ax.set_ylim(0, max(max(estados.values()), 5))  # Ajustar límite superior
    ax.set_title(f"Paso {i+1}")
    ax.set_ylabel("Elementos en la pila")
    ax.set_xlabel("Tipo de pila")

def main():
    global frames, ax
    cadena = input("Ingrese el texto a analizar: ")

    for i in cadena:
        procesar(i)

    print(f"Llaves: {estadoLLaves}, Corchetes: {estadoCorchetes}, Parentesis: {estadoParentesis}, Comillas: {estadoComillas}")

    # Animación
    fig, ax = plt.subplots()  # Definir ax aquí
    ani = animation.FuncAnimation(fig, animar, frames=len(frames), interval=500, repeat=False)
    plt.show()

if __name__ == "__main__":
    main()

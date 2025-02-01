# Autor: Serrano Gayosso Jose Eduardo
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
            print("Pila vacia")
        else:
            self.top = self.top.next

    def display(self):
        if self.isEmpty():
            print("Pila vacia!")
        while not self.isEmpty():
            print(self.top.dato, end=" ")
            self.pop()
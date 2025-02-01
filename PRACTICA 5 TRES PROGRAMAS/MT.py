import random
import tkinter as tk
import time
import math  # Para cálculos de ángulos y posiciones
from collections import defaultdict

class MaquinaDeTuring:
    def __init__(self, cinta, transiciones, estado_inicial, estado_aceptacion):
        self.cinta = list(cinta)  # Convertir la cinta en una lista para fácil manipulación
        self.transiciones = transiciones
        self.estado_actual = estado_inicial
        self.estado_aceptacion = estado_aceptacion
        self.posicion_cabeza = 0

        self.animar = (len(self.cinta) <= 10)  # Solo animar si la longitud <= 10
        if self.animar:
            self.root = tk.Tk()
            self.root.title("Animación de la Máquina de Turing")
            self.canvas = tk.Canvas(self.root, width=600, height=200, bg="white")
            self.canvas.pack()
        else:
            self.root = None
            self.canvas = None

    def paso(self):
        # Obtener el símbolo actual bajo la cabeza
        simbolo_actual = self.cinta[self.posicion_cabeza] if self.posicion_cabeza < len(self.cinta) else 'B'
        
        # Buscar la transición correspondiente
        clave = (self.estado_actual, simbolo_actual)
        if clave not in self.transiciones:
            return False  # No hay transición válida, detenerse
        
        nuevo_estado, nuevo_simbolo, direccion = self.transiciones[clave]
        
        if self.posicion_cabeza < len(self.cinta):
            self.cinta[self.posicion_cabeza] = nuevo_simbolo
        else:
            self.cinta.append(nuevo_simbolo)
        
        if direccion == 'R':
            self.posicion_cabeza += 1
        elif direccion == 'L':
            self.posicion_cabeza -= 1
        
        self.estado_actual = nuevo_estado
        
        if self.animar:
            self.mostrar_cinta()

        return True
    
    def ejecutar(self):
        while self.estado_actual != self.estado_aceptacion:
            if not self.paso():
                print("Máquina detenida: no hay transición válida.")
                print("Cinta final:", ''.join(self.cinta))
                
                if self.animar and self.root is not None:
                    self.root.destroy()
                exit()

            with open("IDs_MT.txt", "a", encoding="utf-8") as archivo:
                archivo.write(f"\n⊦{''.join(self.cinta[:self.posicion_cabeza])}({self.estado_actual}){''.join(self.cinta[self.posicion_cabeza:])}")

        print("Estado de aceptación alcanzado.")
        print("Cinta final:", ''.join(self.cinta))
        
        if self.animar and self.root is not None:
            self.root.destroy()

    def mostrar_cinta(self):
        self.canvas.delete("all")

        x_inicial = 50
        y_inicial = 80
        ancho_celda = 40
        alto_celda = 40

        for i, simbolo in enumerate(self.cinta):
            x1 = x_inicial + i * ancho_celda
            y1 = y_inicial
            x2 = x1 + ancho_celda
            y2 = y1 + alto_celda
            
            if i == self.posicion_cabeza:
                color = "lightblue"
            else:
                color = "white"
            
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
            self.canvas.create_text((x1 + x2)/2, (y1 + y2)/2, text=simbolo, font=("Arial", 16))

        self.canvas.create_text(300, 30, text=f"Estado: {self.estado_actual}", font=("Arial", 14), fill="blue")
        
        self.root.update()
        time.sleep(1)

def graficar_automata(transiciones):

    ventana_automata = tk.Tk()
    ventana_automata.title("Autómata (Diagrama de estados)")

    ancho_canvas = 800
    alto_canvas = 400
    canvas_auto = tk.Canvas(ventana_automata, width=ancho_canvas, height=alto_canvas, bg="white")
    canvas_auto.pack()

    # Posiciones fijas para los estados
    posiciones_estados = {
        'q0': (100, 200),
        'q1': (250, 100),
        'q2': (250, 300),
        'q3': (400, 100),
        'q4': (550, 200)
    }

    radios = 30

    # Dibujamos los estados
    for estado, (cx, cy) in posiciones_estados.items():
        # Si es estado de aceptación, dibujamos doble óvalo
        if estado == 'q4':
            canvas_auto.create_oval(cx - radios - 5, cy - radios - 5,
                                    cx + radios + 5, cy + radios + 5,
                                    outline="blue", width=2)
        # Óvalo base
        canvas_auto.create_oval(cx - radios, cy - radios, cx + radios, cy + radios, fill="lightgray")
        canvas_auto.create_text(cx, cy, text=estado, font=("Arial", 14, "bold"), fill="black")

    # Diccionario para contar cuántos self-loops hay por estado
    self_loop_count = defaultdict(int)

    def dibujar_flecha_arco(cx, cy, etiqueta, offset):
        """
        Dibuja un arco curvado (self-loop) que sale del borde del estado
        y regresa al mismo sin superponerse con otros self-loops.
        """
        # Empezamos en el borde superior del círculo
        x_inicio = cx
        y_inicio = cy - radios
        
        # Ajustamos el offset para separar las curvas
        # Cada self-loop adicional hará que la curva se desplace
        desplazamiento = 40 + offset * 40
        
        # Puntos de control
        x_control1 = cx - (radios + desplazamiento)
        y_control1 = y_inicio - 40 - offset * 10
        x_control2 = cx + (radios + desplazamiento)
        y_control2 = y_inicio - 40 - offset * 10
        
        x_fin = x_inicio
        y_fin = y_inicio
        
        # Trazamos la línea curva (spline) con flecha
        puntos = [
            x_inicio, y_inicio,
            x_control1, y_control1,
            x_control2, y_control2,
            x_fin, y_fin
        ]
        canvas_auto.create_line(
            *puntos,
            fill="black",
            width=2,
            smooth=True,
            arrow=tk.LAST
        )

        # Etiqueta aproximadamente en el punto más alto de la curva
        xm = (x_control1 + x_control2) / 2
        ym = (y_control1 + y_control2) / 2
        canvas_auto.create_text(xm, ym - 15, text=etiqueta, font=("Arial", 10, "bold"), fill="blue")

    def dibujar_flecha(x1, y1, x2, y2, etiqueta):
        """
        Ajusta la línea para que las flechas toquen el borde de los círculos,
        en lugar de sus centros, y coloca la etiqueta en el punto medio.
        """
        angulo = math.atan2(y2 - y1, x2 - x1)
        
        # Ajustamos para que la flecha parta desde el borde del círculo de origen
        x1r = x1 + radios * math.cos(angulo)
        y1r = y1 + radios * math.sin(angulo)
        # Ajustamos para que termine en el borde del círculo de destino
        x2r = x2 - radios * math.cos(angulo)
        y2r = y2 - radios * math.sin(angulo)

        # Dibuja la flecha
        canvas_auto.create_line(x1r, y1r, x2r, y2r, arrow=tk.LAST, width=2)
        
        # Punto medio para la etiqueta
        xm = (x1r + x2r) / 2
        ym = (y1r + y2r) / 2
        canvas_auto.create_text(xm, ym - 10, text=etiqueta, font=("Arial", 10, "bold"), fill="blue")

    # Para reemplazar 'R' o 'L' por flechas reales (→ o ←)
    direccion_a_flecha = {'R': '→', 'L': '←'}

    # Dibujamos las transiciones
    for (estado_origen, simbolo_entrada), (estado_destino, simbolo_salida, direccion) in transiciones.items():
        dir_flecha = direccion_a_flecha.get(direccion, '')
        etiqueta = f"{simbolo_entrada}/{simbolo_salida}{dir_flecha}"

        if estado_origen == estado_destino:
            # Self-loop
            cx, cy = posiciones_estados[estado_origen]
            offset = self_loop_count[estado_origen]
            dibujar_flecha_arco(cx, cy, etiqueta, offset)
            self_loop_count[estado_origen] += 1
        else:
            if (estado_origen in posiciones_estados) and (estado_destino in posiciones_estados):
                x1, y1 = posiciones_estados[estado_origen]
                x2, y2 = posiciones_estados[estado_destino]
                dibujar_flecha(x1, y1, x2, y2, etiqueta)

    ventana_automata.mainloop()

def main():
    print("1. Ingresar cadena\n2. Generar cadena")
    opcion = input("Seleccione una opción: ")
    
    if opcion == "1":
        cadena = input("Ingrese la cadena a analizar: ")
    elif opcion == "2":
        cadena = "".join([str(random.randint(0, 1)) for _ in range(random.randint(1, 1000))])
        print(f"Cadena generada: {cadena}")
    else:
        print("Opción no válida.")
        return
    
    transiciones = {
        ('q0', '0'): ('q1', 'X', 'R'),
        ('q0', 'Y'): ('q3', 'Y', 'R'),
        ('q1', '0'): ('q1', '0', 'R'),
        ('q1', '1'): ('q2', 'Y', 'L'),
        ('q1', 'Y'): ('q1', 'Y', 'R'),
        ('q2', '0'): ('q2', '0', 'L'),
        ('q2', 'X'): ('q0', 'X', 'R'),
        ('q2', 'Y'): ('q2', 'Y', 'L'),
        ('q3', 'Y'): ('q3', 'Y', 'R'),
        ('q3', 'B'): ('q4', 'B', 'R'),
    }

    graficar_automata(transiciones)

    estado_inicial = 'q0'
    estado_aceptacion = 'q4'
    maquina = MaquinaDeTuring(cadena, transiciones, estado_inicial, estado_aceptacion)
    
    with open("IDs_MT.txt", "w", encoding="utf-8") as archivo:
        archivo.write(f"(q0){cadena}")

    maquina.ejecutar()

if __name__ == "__main__":
    main()

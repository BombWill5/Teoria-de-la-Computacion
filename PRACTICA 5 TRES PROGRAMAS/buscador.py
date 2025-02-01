import pandas as pd
import graphviz

def cargar_automata_desde_tabla(ruta_archivo):
    df = pd.read_excel(ruta_archivo)

    estados = df['estado\\simbolo']   # Primera columna tiene los estados
    simbolos = df.columns[1:]         # Todas las demás columnas son símbolos del alfabeto

    automata = {}
    for idx, estado in enumerate(estados):
        automata[estado] = {}
        for simbolo in simbolos:
            automata[estado][simbolo] = df.at[idx, simbolo]

    return automata

def procesar_cadena(automata, cadena, estado_inicial, estados_finales, palabras):
    contador = {palabra: 0 for palabra in palabras.values()} # diccionario
    estado_actual = estado_inicial

    for simbolo in cadena:
        if simbolo not in automata[estado_actual]:
            estado_actual = estado_inicial
            continue
        
        estado_actual = automata[estado_actual][simbolo]

        if estado_actual in estados_finales:
            palabra_encontrada = palabras[estado_actual]
            contador[palabra_encontrada] += 1
            if estado_actual == "κ" or estado_actual == "μ":
                estado_actual = "G"
            else:
                estado_actual = estado_inicial

    return contador


def procesar_archivo(automata, ruta_texto, estado_inicial, estados_finales, palabras, archivo_historia="historia.txt"):
    contador = {palabra: 0 for palabra in palabras.values()}
    posiciones = {palabra: [] for palabra in palabras.values()}

    with open(archivo_historia, "w", encoding="utf-8") as hist:
        hist.write("Historia de Procesamiento del Autómata:\n")
        hist.write("Carácter\tEstadoAnterior\tEstadoSiguiente\tPosición(x,y)\n")

        with open(ruta_texto, "r", encoding="utf-8") as f:
            lineas = f.readlines()

        estado_actual = estado_inicial
        for y, linea in enumerate(lineas, start=1):
            for x, simbolo in enumerate(linea, start=1):
                estado_anterior = estado_actual

                if simbolo not in automata[estado_actual]:
                    estado_actual = estado_inicial
                    hist.write(f"{repr(simbolo)}\t{estado_anterior}\t{estado_actual}\t({x},{y})\n")
                    continue

                estado_siguiente = automata[estado_actual][simbolo]
                estado_actual = estado_siguiente

                hist.write(f"{repr(simbolo)}\t{estado_anterior}\t{estado_siguiente}\t({x},{y})\n")

                if estado_actual in estados_finales:
                    palabra_encontrada = palabras[estado_actual]
                    contador[palabra_encontrada] += 1
                    posiciones[palabra_encontrada].append((x, y))

                    if estado_actual == "κ" or estado_actual == "μ":
                        estado_actual = "G"
                    else:
                        estado_actual = estado_inicial

    return contador, posiciones


def graficar_automata(automata, estado_inicial, estados_finales, nombre_archivo="dfa"):

    dot = graphviz.Digraph(comment="DFA")
    dot.attr(rankdir="LR")  # Orientación de izquierda a derecha

    # Conjunto de todos los estados
    todos_estados = set(automata.keys())

    # Añadir nodos para cada estado
    for estado in todos_estados:
        # Estado final con doble círculo
        if estado in estados_finales:
            dot.node(estado, shape="doublecircle")
        # Estado inicial, en color azul o con algún indicador
        elif estado == estado_inicial:
            dot.node(estado, shape="circle", color="blue")
        else:
            dot.node(estado, shape="circle")

    # Flecha invisible para marcar el estado inicial
    dot.node("ini", shape="point")
    dot.edge("ini", estado_inicial, label="inicio")

    # Añadir transiciones
    for estado in automata:
        for simbolo, siguiente in automata[estado].items():
            dot.edge(estado, siguiente, label=simbolo)

    # Guardar el diagrama en PNG
    dot.render(filename=nombre_archivo, format="png", cleanup=True)
    print(f"Automata guardado en: {nombre_archivo}.png")

def main():
    ruta_archivo = "TablaAutomata.xlsx"
    automata = cargar_automata_desde_tabla(ruta_archivo)

    estado_inicial = "A"
    estados_finales = ["β", "θ", "κ", "λ", "μ", "ξ"]
    palabras = {
        "β": "Acoso",
        "θ": "Acecho",
        "λ": "Agresión",
        "κ": "Víctima",
        "ξ": "Violación",
        "μ": "Machista"
    }

    cadena = "victima, victimacecho Víctimagresion Victimacosovíctimachistacoso"
    resultado = procesar_cadena(automata, cadena, estado_inicial, estados_finales, palabras)

    print("Conteo de palabras encontradas (modo cadena directa):")
    for palabra, conteo in resultado.items():
        print(f"{palabra}: {conteo}")

    archivo_entrada = "texto_entrada.txt"
    archivo_salida_historia = "historia.txt"    

    print("\nProcesando el archivo de texto...")

    conteo_archivo, posiciones_archivo = procesar_archivo(
        automata,
        archivo_entrada,
        estado_inicial,
        estados_finales,
        palabras,
        archivo_historia=archivo_salida_historia
    )

    print("Conteo de palabras encontradas en el archivo:")
    for palabra, cant in conteo_archivo.items():
        print(f"{palabra}: {cant}")

    print("\nPosiciones donde se encontraron las palabras en el archivo:")
    for palabra, lista_posiciones in posiciones_archivo.items():
        if lista_posiciones:
            print(f"Palabra: {palabra}")
            for (x, y) in lista_posiciones:
                print(f"  - Encontrada en (x={x}, y={y})")


    print("\nGenerando imagen del autómata...")
    graficar_automata(automata, estado_inicial, estados_finales, nombre_archivo="dfa")

if __name__ == "__main__":
    main()
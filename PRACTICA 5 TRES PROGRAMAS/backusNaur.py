import random

def main():
    print("1. Ingresar cantidad de Ifs\n2. Dejar que la máquina decida")
    opc = input("Seleccione una opción: ")
    if opc == "1":
        while True:
            ifs = int(input("Ingrese la cantidad de Ifs a realizar:"))
            if ifs >= 0 and ifs <= 1000:
                break
    elif opc == "2":
        ifs = random.randint(1, 1000)

    print(f"Ifs a realizar: {ifs}")
    

    contadorIf = 0
    contadorDeriv = 0
    derivaciones = "S"
    with open("derivaciones.txt", "w", encoding="utf-8") as archivo:
        archivo.write(f"S\n")
    print(derivaciones)


    while contadorIf != ifs and contadorDeriv < 1000:
        if contadorIf == 0:
            variable = "S"
        else:
            variable = random.choice(["S", "A"])

        indice = -1
        indices = []
        while True:
            indice = derivaciones.find(variable, indice + 1)  # Buscar desde el índice siguiente
            if indice == -1:  # Si no se encuentra más ocurrencias, termina
                if indices == []:
                    variable = "S"
                    continue
                else:
                    break
            indices.append(indice)

        indice = random.choice(indices)   

        if variable == "S":
            derivaciones = derivaciones[:indice] + "iCtSA" + derivaciones[indice + 1:]
            contadorIf += 1
            contadorDeriv += 1
        elif variable == "A":
            if (indice + 1) < len(derivaciones):
                if derivaciones[indice + 1] == "A":
                    derivaciones = derivaciones[:indice] + "" + derivaciones[indice + 1:]
            else:
                derivaciones = derivaciones[:indice] + random.choice(["eS", ""]) + derivaciones[indice + 1:]
            contadorDeriv += 1
        
        print(f"Variable a derivar: {variable}")
        print(derivaciones)
        with open("derivaciones.txt", "a", encoding="utf-8") as archivo:
            archivo.write(f"=> {derivaciones}\n")

    #Reemplazar las A restantes por epsilon
    derivaciones = derivaciones.replace("A", "")
    with open("derivaciones.txt", "a", encoding="utf-8") as archivo:
            archivo.write(f"=>* {derivaciones}\n")


    with open("pseudocodigo.txt", "w", encoding="utf-8") as archivo:
                archivo.write("")

    contadorTabs = 0
    pseudocodigo = []  # Lista para guardar el pseudocódigo
    for i in derivaciones:
        line = ""
        if i == "i":
            line = "\t" * contadorTabs + "if"
        elif i == "C":
            line = "(condition)"
        elif i == "t":
            line = "{\n"
            contadorTabs += 1
        elif i == "S":
            contadorTabs -= 1
            line = "\t" * (contadorTabs + 1) + "Statement\n" + "\t" * contadorTabs + "}\n"
        elif i == "e":
            line = "\t" * contadorTabs + "else{\n"
            contadorTabs += 1
        pseudocodigo.append(line)
    for i in range(contadorTabs):
        contadorTabs -= 1
        pseudocodigo.append("\t" * contadorTabs + "}\n")

    with open("pseudocodigo.txt", "w", encoding="utf-8") as archivo:
        archivo.writelines(pseudocodigo)




if __name__ == "__main__":
    main()

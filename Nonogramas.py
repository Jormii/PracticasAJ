def inicializar_nonograma():
    filas_columnas = input().strip().split()
    n_filas = int(filas_columnas[0])
    n_columnas = int(filas_columnas[1])

    filas = [0] * n_filas
    columnas = [0] * n_columnas
    columnas_invalidas = [-1] * n_columnas
    nonograma = []

    fi_total = 0
    fis = input().strip().split()
    for f in range(n_filas):
        filas[f] = int(fis[f])
        nonograma.append([0] * n_columnas)

    cis = input().strip().split()
    for c in range(n_columnas):
        columnas[c] = int(cis[c])
        if columnas[c] == 0:
            columnas_invalidas[c] = -2

    solucion = {}
    
    solucion["n_filas"] = n_filas
    solucion["filas"] = filas                               # Valores originales de las filas. Constante
    
    solucion["n_columnas"] = n_columnas
    solucion["columnas"] = columnas                         # Cuantas celdas quedan por pintar en las columnas
    solucion["columnas_pintadas"] = [-1] * n_columnas       # Indica en que filas comenzaron a pintarse las columnas
    solucion["columnas_invalidas"] = columnas_invalidas     # Vector que almacena si se puede pintar en una columna.
                                                            # Almacena en que fila se invalido. Se usa un valor -2 para indicar
                                                            # que la columna vale originalmente 0
    
    solucion["nonograma"] = nonograma                       # Matriz de 0s y 1s que representa el nonograma. 1 indica que se pinta una celda

    return solucion


# Un nonograma es solución cuando se han visitado todas sus filas
def es_solucion(nonograma, d):
    return d >= nonograma["n_filas"]


def es_factible(nonograma, fila, columna):
    valor_fila = nonograma["filas"][fila]
    ultima_columna = columna + valor_fila
    for c in range(columna, ultima_columna):
        # Si la columna no es valida
        if nonograma["columnas_invalidas"][c] != -1:
            return False

        # Si se ha pintado en esta columa y la celda inmediatamente superior no se ha pintado => Habria un espacio entre columnas
        if nonograma["columnas_pintadas"][c] != -1 and nonograma["nonograma"][fila - 1][c] != 1:
            return False

    return True


def actualizar_valores(nonograma, fila, columna):
    valor_fila = nonograma["filas"][fila]
    ultima_columna = columna + valor_fila
    for c in range(columna, ultima_columna):
        nonograma["nonograma"][fila][c] = 1
        nonograma["columnas"][c] -= 1

        if nonograma["columnas_pintadas"][c] == -1:
            nonograma["columnas_pintadas"][c] = fila

        # Si ya se ha pintado toda la columna, entonces no es valida
        if nonograma["columnas"][c] == 0:
            nonograma["columnas_invalidas"][c] = fila

    # Comprobar si se han invalidado columnas. No tiene sentido comprobar invalidaciones en la primera fila
    if fila != 0:        
        for c in range(nonograma["n_columnas"]):
            # Si la columna ya no es valida o nunca se ha pintado en ella, pasar a la siguiente            
            if nonograma["columnas_invalidas"][c] != -1 or nonograma["columnas_pintadas"][c] == -1:
                continue
            
            # Se invalida una columna si se deja
            esta_columa_pintada = nonograma["nonograma"][fila][c] == 1
            esta_columna_fila_anterior_pintada = nonograma["nonograma"][fila - 1][c] == 1
            if not esta_columa_pintada and esta_columna_fila_anterior_pintada:
                nonograma["columnas_invalidas"][c] = fila


def revertir_actualizacion(nonograma, fila, columna):
    valor_fila = nonograma["filas"][fila]
    ultima_columna = columna + valor_fila
    for c in range(columna, ultima_columna):
        nonograma["nonograma"][fila][c] = 0
        nonograma["columnas"][c] += 1

        if nonograma["columnas_pintadas"][c] == fila:
            nonograma["columnas_pintadas"][c] = -1

    # Deshacer invalidaciones
    for c in range(nonograma["n_columnas"]):
        if nonograma["columnas_invalidas"][c] == fila:
            nonograma["columnas_invalidas"][c] = -1


def resolver_nonograma(nonograma, d=0):
    if es_solucion(nonograma, d):
        return nonograma, True

    # Se resuelve la siguiente fila si no hay nada que pintar en esta
    fila = d
    if nonograma["filas"][fila] == 0:
        return resolver_nonograma(nonograma, d + 1)

    i = 0
    es_sol = False
    valor_fila = nonograma["filas"][fila]
    columna_maxima = nonograma["n_columnas"] - valor_fila
    while not es_sol and i <= columna_maxima:
        columna = i
        
        if es_factible(nonograma, fila, columna):
            actualizar_valores(nonograma, fila, columna)
            nonograma, es_sol = resolver_nonograma(nonograma, d + 1)
            if not es_sol:
                revertir_actualizacion(nonograma, fila, columna)

        i += 1

    return nonograma, es_sol


def print_nonograma(solucion):
    for fila in solucion["nonograma"]:
        for c in fila:
            print("#" if c == 1 else "-", end="")
        print()


nonograma = inicializar_nonograma()
solucion, es_sol = resolver_nonograma(nonograma)
if es_sol:
    print_nonograma(solucion)
else:
    print("IMPOSIBLE")

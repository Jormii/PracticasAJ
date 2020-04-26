def inicializar_nonograma():
    filas_columnas = input().strip().split()
    n_filas = int(filas_columnas[0])
    n_columnas = int(filas_columnas[1])

    filas = [0] * n_filas
    columnas = [0] * n_columnas
    nonograma = []

    fis = input().strip().split()
    for f in range(n_filas):
        filas[f] = int(fis[f])
        nonograma.append([0] * n_columnas)

    cis = input().strip().split()
    for c in range(n_columnas):
        columnas[c] = int(cis[c])

    solucion = {}

    solucion["n_filas"] = n_filas
    solucion["filas_constante"] = filas                 # Valores originales de las filas
    solucion["filas"] = list(filas)                     # Valores que restan para completar la fila
    solucion["filas_pintadas"] = [-1] * n_filas         # Indica la primera columna en la que se comenzó a pintar las filas
    solucion["filas_primera_celda"] = [-1] * n_filas    # Primera celda pintada de cada fila

    solucion["n_columnas"] = n_columnas
    solucion["columnas_constante"] = list(columnas)
    solucion["columnas"] = columnas
    solucion["columnas_pintadas"] = [-1] * n_columnas   # Indica la fila en la que se comenzó a pintar las columnas

    solucion["nonograma"] = nonograma                   # Matriz de 0s y 1s que representa el nonograma. 1 indica que se pinta una celda

    return solucion


# Se ha resuelto cuando se han pintado todas las filas
# No se comprueban las columnas porque se garantiza se han pintado todas
def es_solucion(nonograma):
    for valor_fila in nonograma["filas"]:
        if valor_fila != 0:
            return False

    return True


# Devuelve una lista de columnas para las que tiene sentido comprobar si se puede insertar la fila
def calcular_columnas_validas(nonograma, fila):
    valor_fila = nonograma["filas"][fila]
    
    # Si esta fila ya se ha pintado
    if nonograma["filas_pintadas"][fila] != -1:
        valor_fila_constante = nonograma["filas_constante"][fila]
        columna_pintada = nonograma["filas_pintadas"][fila]
            
        # Se busca la primera celda pintada en la fila
        primera_celda_fila = columna_pintada
        for c in range(columna_pintada - 1, -1, -1):
            if nonograma["nonograma"][fila][c] == 0:
                break
            
            primera_celda_fila -= 1
            
        columna_inicial = max(0, primera_celda_fila - valor_fila)
        columna_maxima = min(primera_celda_fila, nonograma["n_columnas"] - valor_fila_constante)
    else:
        columna_inicial = 0
        columna_maxima = nonograma["n_columnas"] - valor_fila   # En este caso valor_fila == valor_fila_cte

    return list(range(columna_inicial, columna_maxima + 1))


def es_factible(nonograma, fila, columna):
    # Dado que es_solucion no tiene en consideracion las filas
    if fila > nonograma["n_filas"]:
        return False

    # Si se han pintado mas celdas de las que se debian
    valor_fila = nonograma["filas"][fila]
    if valor_fila < 0:
        return False

    # Por cada una de las columnas afectadas si se pintara esta fila
    valor_fila_constante = nonograma["filas_constante"][fila]
    ultima_columna = columna + valor_fila_constante
    for c in range(columna, ultima_columna):
        # Ignorar columna si ya se ha pintado
        if nonograma["nonograma"][fila][c] == 1:
            continue

        # Si previamente ya se ha pintado la columna entera o si pintar esta columna supondría exceder el nonograma
        valor_columna = nonograma["columnas"][c]
        if valor_columna == 0 or fila + valor_columna > nonograma["n_filas"]:
            return False

    return True


def actualizar_valores(nonograma, fila, columna):
    # Por cada una de las columnas que se van a pintar
    valor_fila_constante = nonograma["filas_constante"][fila]
    ultima_columna = columna + valor_fila_constante
    for c in range(columna, ultima_columna):
        # No se hace nada si ya se ha pintado en esta columna
        if nonograma["columnas_pintadas"][c] != -1:
            continue

        nonograma["columnas_pintadas"][c] = fila

        # Se vuelca la columna
        valor_columna = nonograma["columnas"][c]
        for f in range(fila, fila + valor_columna):
            if nonograma["filas_pintadas"][f] == -1:
                nonograma["filas_pintadas"][f] = c

            nonograma["nonograma"][f][c] = 1
            nonograma["filas"][f] -= 1
            nonograma["columnas"][c] -= 1


def revertir_actualizacion(nonograma, fila, columna):
    # Por cada una de las columnas que se van a desactualizar
    valor_fila_constante = nonograma["filas_constante"][fila]
    ultima_columna = columna + valor_fila_constante
    for c in range(columna, ultima_columna):
        # Si la columna no se volco en esta fila, continuar
        if nonograma["columnas_pintadas"][c] != fila:
            continue

        nonograma["columnas_pintadas"][c] = -1

        # Se "desdibuja" la columna
        valor_columna = nonograma["columnas_constante"][c]
        for f in range(fila, fila + valor_columna):
            if nonograma["filas_pintadas"][f] == c:
                nonograma["filas_pintadas"][f] = -1

            nonograma["nonograma"][f][c] = 0
            nonograma["filas"][f] += 1
            nonograma["columnas"][c] += 1


def resolver_nonograma(nonograma, d=0):
    if es_solucion(nonograma):
        return nonograma, True

    # Se pasa a la siguiente fila si no hay nada que pintar
    fila = d
    if nonograma["filas"][fila] == 0:
        return resolver_nonograma(nonograma, d + 1)

    i = 0
    es_sol = False
    columnas_validas = calcular_columnas_validas(nonograma, fila)
    while not es_sol and i < len(columnas_validas):
        columna = columnas_validas[i]

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
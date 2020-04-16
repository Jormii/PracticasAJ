import time


def inicializar_nonograma():
    filas_columnas = input().strip().split()
    n_filas = int(filas_columnas[0])
    n_columnas = int(filas_columnas[1])

    filas = [0] * n_filas
    columnas = [0] * n_columnas

    fi_total = 0
    fis = input().strip().split()
    for f in range(n_filas):
        filas[f] = int(fis[f])

    cis = input().strip().split()
    for c in range(n_columnas):
        columnas[c] = int(cis[c])

    solucion = {}
    solucion["n_filas"] = n_filas
    solucion["filas"] = filas
    solucion["n_columnas"] = n_columnas
    solucion["columnas"] = columnas
    solucion["columnas_pintadas"] = [-1] * n_columnas
    solucion["columnas_invalidas"] = [-1] * n_columnas
    solucion["nonograma"] = [-1] * n_filas

    return solucion


def es_solucion(nonograma, d):
    return d >= nonograma["n_filas"]


def calcular_columnas_validas(nonograma, fila):
    valor_fila = nonograma["filas"][fila]
    columna_inicial = 0
    columna_maxima = nonograma["n_columnas"] - valor_fila
    return list(range(columna_inicial, columna_maxima + 1))


def es_factible(nonograma, fila, columna):
    if fila == 0:
        solucion_previa = (0, nonograma["n_columnas"] - 1)
    else:
        solucion_previa = nonograma["nonograma"][fila - 1]

    valor_fila = nonograma["filas"][fila]
    ultima_columna = columna + valor_fila
    for c in range(columna, ultima_columna):
        valor_columna = nonograma["columnas"][c]
        if valor_columna == 0:
            return False

        if nonograma["columnas_pintadas"][c] != -1:
            if solucion_previa == -1:
                return False
            
            if c not in range(solucion_previa[0], solucion_previa[1] + 1):
                return False

    return True


def actualizar_valores(nonograma, fila, columna):
    valor_fila = nonograma["filas"][fila]
    ultima_columna = columna + valor_fila
    for c in range(columna, ultima_columna):
        nonograma["columnas"][c] -= 1
        if nonograma["columnas_pintadas"][c] == -1:
            nonograma["columnas_pintadas"][c] = fila

    nonograma["nonograma"][fila] = (columna, ultima_columna - 1)


def revertir_actualizacion(nonograma, fila, columna):
    valor_fila = nonograma["filas"][fila]
    ultima_columna = columna + valor_fila
    for c in range(columna, ultima_columna):
        nonograma["columnas"][c] += 1
        if nonograma["columnas_pintadas"][c] == fila:
            nonograma["columnas_pintadas"][c] = -1

    nonograma["nonograma"][fila] = -1


def resolver_nonograma(nonograma, d=0):
    if es_solucion(nonograma, d):
        return nonograma, True

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
            solucion, es_sol = resolver_nonograma(nonograma, d + 1)
            if not es_sol:
                revertir_actualizacion(nonograma, fila, columna)

        i += 1

    return nonograma, es_sol


def print_nonograma(solucion):
    for f in range(solucion["n_filas"]):
        solucion_fila = solucion["nonograma"][f]
        for c in range(solucion["n_columnas"]):
            if solucion_fila == -1:
                print("-", end="")
            else:
                print("#" if c in range(
                    solucion_fila[0], solucion_fila[1] + 1) else "-", end="")
        print()


nonograma = inicializar_nonograma()

start = time.time()
solucion, es_sol = resolver_nonograma(nonograma)
end = time.time()
if es_sol:
    print_nonograma(solucion)
else:
    print("IMPOSIBLE")
print("Segundos:", end - start)
print("Milisegundos:", (end - start) * 1000)

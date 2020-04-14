import time


def inicializar_nonograma():
    filas_columnas = input().strip().split()
    n_filas = int(filas_columnas[0])
    n_columnas = int(filas_columnas[1])

    filas = [0] * n_filas
    columnas = [0] * n_columnas
    nonograma = []

    fi_total = 0
    fis = input().strip().split()
    for f in range(n_filas):
        filas[f] = int(fis[f])
        nonograma.append([0] * n_columnas)

    cis = input().strip().split()
    for c in range(n_columnas):
        columnas[c] = int(cis[c])

    solucion = {}
    
    solucion["n_filas"] = n_filas
    solucion["filas"] = list(filas)
    solucion["filas_constante"] = filas
    solucion["filas_pintadas"] = [-1] * n_filas
    
    solucion["n_columnas"] = n_columnas
    solucion["columnas"] = columnas
    solucion["columnas_constante"] = list(columnas)
    solucion["columnas_pintadas"] = [-1] * n_columnas
    
    solucion["nonograma"] = nonograma

    return solucion


def es_solucion(nonograma, d):
    return d >= nonograma["n_filas"]


def calcular_columnas_validas(nonograma, fila):
    valor_fila = nonograma["filas"][fila]
    if nonograma["filas_pintadas"][fila] != -1:
        columna_pintada = nonograma["filas_pintadas"][fila]
        columna_inicial = max(columna_pintada - valor_fila, 0)
        columna_maxima = columna_pintada
        if columna_maxima > nonograma["n_columnas"] - valor_fila:
            columna_maxima = nonograma["n_columnas"] - valor_fila
    else:
        columna_inicial = 0
        columna_maxima = nonograma["n_columnas"] - valor_fila

    return list(range(columna_inicial, columna_maxima + 1))


def es_factible(nonograma, fila, columna):
    valor_fila = nonograma["filas"][fila]
    if valor_fila < 0:
        return False
    
    valor_fila_constante = nonograma["filas_constante"][fila]
    ultima_columna = columna + valor_fila_constante
    for c in range(columna, ultima_columna):
        valor_columna = nonograma["columnas"][c]
        
        if nonograma["nonograma"][fila][c] == 1:
            if valor_columna >= fila:
                return False
            else:
                continue

        if valor_columna == 0:
            return False

    return True


def actualizar_valores(nonograma, fila, columna):
    nonograma["filas"][fila] = 0
    if nonograma["filas_pintadas"][fila] == -1:
        nonograma["filas_pintadas"][fila] = columna
    
    valor_fila_constante = nonograma["filas_constante"][fila]
    ultima_columna = columna + valor_fila_constante
    for c in range(columna, ultima_columna):
        if nonograma["nonograma"][fila][c] != 1:
            nonograma["columnas"][c] -= 1

            if nonograma["columnas_pintadas"][c] == -1:
                nonograma["columnas_pintadas"][c] = fila
                
                valor_columna = nonograma["columnas"][c]
                for f in range(fila + 1, fila + 1 + valor_columna):
                    if nonograma["filas_pintadas"][f] == -1:
                        nonograma["filas_pintadas"][f] = c
                    
                    nonograma["nonograma"][f][c] = 1
                    nonograma["filas"][f] -= 1
                nonograma["columnas"][c] = 0
                
        nonograma["nonograma"][fila][c] = 1


def revertir_actualizacion(nonograma, fila, columna):
    nonograma["filas"][fila] = nonograma["filas_constante"][fila]
    if nonograma["filas_pintadas"][fila] == columna:
        nonograma["filas_pintadas"][fila] = -1
        
    valor_fila_constante = nonograma["filas_constante"][fila]
    ultima_columna = columna + valor_fila_constante
    for c in range(columna, ultima_columna):
        nonograma["columnas"][c] += 1

        if nonograma["columnas_pintadas"][c] == fila:
            nonograma["columnas_pintadas"][c] = -1
            
            valor_columna = nonograma["columnas_constante"][c]
            for f in range(fila + 1, fila + valor_columna):
                if nonograma["filas_pintadas"][f] == c:
                    nonograma["filas_pintadas"][f] = -1
                
                nonograma["nonograma"][f][c] = 0
                nonograma["filas"][f] += 1
                nonograma["columnas"][c] += 1

        nonograma["nonograma"][fila][c] = 0


def resolver_nonograma(nonograma, d=0):
    if es_solucion(nonograma, d):
        return nonograma, True

    fila = d
    if nonograma["filas_constante"][fila] == 0:
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

start = time.time()
solucion, es_sol = resolver_nonograma(nonograma)
end = time.time()
if es_sol:
    print_nonograma(solucion)
else:
    print("IMPOSIBLE")
print("Segundos:", end - start)
print("Milisegundos:", (end - start) * 1000)

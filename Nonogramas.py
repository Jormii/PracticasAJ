def inicializar_nonograma():
    filas_columnas = input().strip().split()
    n_filas = int(filas_columnas[0])
    n_columnas = int(filas_columnas[1])

    nonograma = []
    filas = [0] * n_filas
    columnas = [0] * n_columnas

    fi_total = 0
    fis = input().strip().split()
    for f in range(n_filas):
        fi = int(fis[f])
        fi_total += fi
        filas[f] = fi

        nonograma.append([-1] * n_columnas)

    ci_total = 0
    cis = input().strip().split()
    for c in range(n_columnas):
        ci = int(cis[c])
        ci_total += ci
        columnas[c] = ci

    solucion = {}
    solucion["n_filas"] = n_filas
    solucion["fi_total"] = fi_total
    solucion["filas"] = filas
    solucion["n_columnas"] = n_columnas
    solucion["ci_total"] = ci_total
    solucion["columnas"] = columnas
    solucion["columnas_pintadas"] = [-1] * n_columnas
    solucion["nonograma"] = nonograma

    return solucion


def es_solucion(nonograma):
    return (nonograma["fi_total"] + nonograma["ci_total"]) == 0


def es_factible(nonograma, fila, columna):
    if fila >= nonograma["n_filas"]:
        return False
    
    valor_fila = nonograma["filas"][fila]
    ultima_columna = columna + valor_fila
    for c in range(columna, ultima_columna):
        valor_columna = nonograma["columnas"][c]
        if valor_columna == 0:
            return False
        
        if nonograma["columnas_pintadas"][c] != -1:
            if nonograma["nonograma"][fila - 1][c] != 1:
                return False

    return True

def resolver_nonograma(nonograma, d=0):
    if es_solucion(nonograma):
        return nonograma, True

    fila = d
    valor_fila = nonograma["filas"][fila]
    columna = 0
    columna_limite = nonograma["n_columnas"] - valor_fila
    es_sol = False
    while not es_sol and columna <= columna_limite:
        if es_factible(nonograma, fila, columna):
            nonograma["fi_total"] -= valor_fila
            nonograma["ci_total"] -= valor_fila
            
            ultima_columna = columna + valor_fila
            for c in range(columna, ultima_columna):
                if nonograma["columnas_pintadas"][c] == -1:
                    nonograma["columnas_pintadas"][c] = fila
                nonograma["filas"][fila] -= 1   # Innecesario
                nonograma["columnas"][c] -= 1
                nonograma["nonograma"][fila][c] = 1

            solucion, es_sol = resolver_nonograma(nonograma, d + 1)
            
            if not es_sol:
                nonograma["fi_total"] += valor_fila
                nonograma["ci_total"] += valor_fila
                for c in range(columna, ultima_columna):
                    if nonograma["columnas_pintadas"][c] == fila:
                        nonograma["columnas_pintadas"][c] = -1
                    nonograma["filas"][fila] += 1   # Innecesario
                    nonograma["columnas"][c] += 1
                    nonograma["nonograma"][fila][c] = -1
        
        columna += 1

    return nonograma, es_sol

def print_nonograma(solucion):
    nonograma = solucion["nonograma"]
    for fila in nonograma:
        for columna in fila:
            print("#" if columna == 1 else "-", end="")
        print()

import time

nonograma = inicializar_nonograma()

start = time.time()
solucion, es_sol = resolver_nonograma(nonograma)
end = time.time()
if es_sol:
    print_nonograma(solucion)
else:
    print("IMPOSIBLE")
print((end - start) * 1000)

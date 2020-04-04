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
    solucion["nonograma"] = nonograma

    return solucion


def es_solucion(nonograma):
    return (nonograma["fi_total"] + nonograma["ci_total"]) == 0


def es_factible(nonograma, fila, columna, pintar):
    if fila >= nonograma["n_filas"]:
        return False
    
    valor_fila = nonograma["filas"][fila]
    valor_columna = nonograma["columnas"][columna]
    
    return valor_fila >= pintar and valor_columna >= pintar

def resolver_nonograma(nonograma, d=0):
    if es_solucion(nonograma):
        return nonograma, True

    fila = d // nonograma["n_filas"]
    columna = d % nonograma["n_filas"]

    es_sol = False
    pintar = 1
    while not es_sol and pintar >= 0:
        if es_factible(nonograma, fila, columna, pintar):
            nonograma["fi_total"] -= pintar
            nonograma["ci_total"] -= pintar
            nonograma["filas"][fila] -= pintar
            nonograma["columnas"][columna] -= pintar
            nonograma["nonograma"][fila][columna] = pintar

            solucion, es_sol = resolver_nonograma(nonograma, d + 1)
            
            if not es_sol:
                nonograma["fi_total"] += pintar
                nonograma["ci_total"] += pintar
                nonograma["filas"][fila] += pintar
                nonograma["columnas"][columna] += pintar
                nonograma["nonograma"][fila][columna] = -1
        
        pintar -= 1

    return nonograma, es_sol

def print_nonograma(solucion):
    nonograma = solucion["nonograma"]
    for fila in nonograma:
        for columna in fila:
            print("#" if columna == 1 else "-", end="")
        print()


nonograma = inicializar_nonograma()
solucion, es_sol = resolver_nonograma(nonograma)
if es_sol:
    print_nonograma(solucion)
else:
    print("IMPOSIBLE")

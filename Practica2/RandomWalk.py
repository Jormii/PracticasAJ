import random  # TODO: Aleatorios vistos en clase

direcciones = {
    0: (-1, 0),    # Norte
    1: (0, 1),     # Este
    2: (1, 0),     # Sur
    3: (0, -1)     # Oeste
}


def random_walk(ancho, alto, n_tuneles, l_max_tunel):
    # Crear mapa
    mapa = []
    for i in range(alto):
        mapa.append([0] * ancho)

    # Elegir posicion aleatoria
    random.seed(None)

    fila = random.randint(0, alto - 1)
    columna = random.randint(0, ancho - 1)

    posicion_inicio = (fila, columna)
    mapa[fila][columna] = 2

    # Crear tuneles
    for i in range(n_tuneles):
        l = random.randint(1, l_max_tunel)
        l_hasta_giro = random.randint(1, l)
        direccion_indice = random.randint(0, 3)
        direccion = direcciones[direccion_indice]

        fila = posicion_inicio[0]
        columna = posicion_inicio[1]
        j = 1
        while j <= l:
            fila += direccion[0]
            columna += direccion[1]

            # Si sale del mapa, girar en el sentido de las agujas del reloj
            if fila < 0 or fila >= alto or columna < 0 or columna >= ancho:
                # Deshacer
                fila -= direccion[0]
                columna -= direccion[1]
                
                # Avanzar en la nueva direccion
                direccion_indice = (direccion_indice + 1) % 4
                direccion = direcciones[direccion_indice]
                
                continue

            # Si se ha recorrido tanto como para girar
            # if j == l_hasta_giro:
                # direccion_indice = (direccion_indice + 1) % 4
                # direccion = direcciones[direccion_indice]

            # Pintar si no es la casilla de inicio
            if mapa[fila][columna] != 2:
                mapa[fila][columna] = 1

            j+= 1

    return mapa


def imprimir_mapa(mapa):
    for fila in mapa:
        for columna in fila:
            print(columna, "", end="")
        print("")

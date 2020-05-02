import random  # TODO: Aleatorios vistos en clase

direcciones = {
    0: (0, -1),    # Norte
    1: (1, 0),     # Este
    2: (0, 1),     # Sur
    3: (-1, 0)     # Oeste
}


def random_walk(ancho, alto, n_tuneles, l_max_tunel, debug=False):
    # Crear mapa
    mapa = []
    for i in range(alto):
        mapa.append([0] * ancho)

    if debug:
        print("[DEBUG] Creando mapa de {0}x{1}".format(ancho, alto))
        print("[DEBUG] Mapa:")
        imprimir_mapa(mapa)

    # Calcular posicion inicial
    random.seed(None)
    x0 = random.randint(0, ancho - 1)
    y0 = random.randint(0, alto - 1)

    if debug:
        print("[DEBUG] Posicion inicial ({0}, {1})".format(x0, y0))

    # Dibujar tuneles
    for t in range(n_tuneles):
        longitud = random.randint(1, l_max_tunel)
        punto_giro = random.randint(1, longitud)
        direccion = direcciones[random.randint(0, 3)]

        if debug:
            print("[DEBUG] Pintando tunel numero {0}".format(t + 1))
            print("[DEBUG] Longitud del tunel: {0}".format(longitud))
            print("[DEBUG] Punto de giro del tunel: {0}".format(punto_giro))
            print("[DEBUG] Direccion del tunel: {0}".format(direccion))

        x = x0
        y = y0
        for paso in range(1, longitud + 1):
            while se_saldria_del_mapa(ancho, alto, x, y, direccion):
                direccion = calcular_nueva_direccion(
                    ancho, alto, x, y, direccion)

                if debug:
                    print("[DEBUG] El tunel ha alcanzado una pared. Nueva direccion: {0}".format(
                        direccion))

            x += direccion[0]
            y += direccion[1]
            mapa[y][x] = 1

            if debug:
                print(
                    "[DEBUG] Se ha pintado un tunel en ({0}, {1})".format(x, y))

            if paso == punto_giro:
                direccion = calcular_nueva_direccion(
                    ancho, alto, x, y, direccion)

                if debug:
                    print("[DEBUG] Se ha alcanzado el punto de giro. Nueva direccion: {0}".format(
                        direccion))

    # Para indicar la posicion inicial en el mapa devuelto
    mapa[y0][x0] = "*"
    return mapa


def se_saldria_del_mapa(ancho, alto, x, y, direccion):
    x += direccion[0]
    y += direccion[1]

    return x < 0 or y < 0 or x >= ancho or y >= alto


def calcular_nueva_direccion(ancho, alto, x, y, direccion):
    # Se mueve hacia el norte o sur
    if direccion[0] == 0:
        porcentaje_en_x = x / ancho # %x € [0, 1], si extremo izquierdo/derecho
        girar_derecha = random.random() >= porcentaje_en_x
        nueva_direccion = direcciones[1] if girar_derecha else direcciones[3]
    # Se mueve hacia el oeste o este
    else:
        porcentaje_en_y = y / alto # %y € [0, 1], si extremo superior/inferior
        girar_abajo = random.random() >= porcentaje_en_y
        nueva_direccion = direcciones[2] if girar_abajo else direcciones[0]

    return nueva_direccion


def imprimir_mapa(mapa):
    for fila in mapa:
        for columna in fila:
            print(columna, "", end="")
        print("")

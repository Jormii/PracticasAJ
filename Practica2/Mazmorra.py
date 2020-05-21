import importlib

i_casilla = importlib.import_module("Casilla")
i_habitacion = importlib.import_module("Habitacion")
i_vegas = importlib.import_module("LasVegas")
i_matriz_utils = importlib.import_module("MatrizUtils")


class Mazmorra(object):
    def __init__(self, template, factor, densidad_maxima, lista_tesoros, debug=False):
        self.template = template
        self.factor = factor
        self.densidad_maxima = densidad_maxima
        self.lista_tesoros = lista_tesoros
        self.debug = debug

        self.ancho = template.ancho * factor
        self.alto = template.alto * factor
        self.mazmorra = []
        self.habitaciones = {}
        self.celdas_ocupadas = 0
        self.densidad = 0

    def generar_mazmorra(self):
        self.inicializar_mazmorra()
        x0, y0 = self.obtener_posicion_inicial()

        # Crear y añadir contenido a la mazmorra
        self.crear_mazmorra_a_partir_de_mapa(x0, y0)
        self.expandir_mazmorra()
        self.crear_tesoros()

        # Obtener casillas adyacentes para posteriormente dibujar los sprites
        for fila in self.mazmorra:
            for casilla in fila:
                casilla.calcular_conexiones(
                    self.mazmorra, self.ancho, self.alto)

        return self.mazmorra

    def inicializar_mazmorra(self):
        # Reiniciar variables
        self.mazmorra.clear()
        self.habitaciones.clear()
        self.celdas_ocupadas = 1    # Casilla inicial

        # Generar mazmorra
        self.alto = self.template.alto * self.factor
        self.ancho = self.template.ancho * self.factor
        for y in range(self.alto):
            self.mazmorra.append([0] * self.ancho)
            for x in range(self.ancho):
                posicion = (x, y)
                casilla = i_casilla.Casilla(posicion)
                self.mazmorra[y][x] = casilla

        # En caso de que se llame antes a generar el mapa
        if not self.template.casilla_inicial:
            self.template.random_walk()

    def obtener_posicion_inicial(self):
        posicion_inicial_mapa = self.template.casilla_inicial.posicion
        x0 = self.convertir_mapa_mazmorra(posicion_inicial_mapa[0])
        y0 = self.convertir_mapa_mazmorra(posicion_inicial_mapa[1])

        if self.debug:
            print("[DEBUG:Mazmorra]")
            print(
                "[DEBUG] Creando mazmorra a partir de la posicion ({0}, {1})".format(x0, y0))

        return x0, y0

    def crear_mazmorra_a_partir_de_mapa(self, x0, y0):
        if self.debug:
            print("[DEBUG] Traduciendo mapa a mazmorra")

        self.crear_habitacion(x0, y0, inicial=True)

        casillas_visitadas = set()
        casillas_visitadas.add((x0, y0))

        for direccion in self.template.casilla_inicial.conexiones:
            self.pintar_tunel_a_partir_de_mapa(
                x0, y0, direccion, casillas_visitadas)

    def pintar_tunel_a_partir_de_mapa(self, x, y, direccion, casillas_visitadas):
        if self.debug:
            print("[DEBUG] Pintando tunel desde ({0}, {1}) en direccion {2}".format(
                x, y, direccion))

        # Crear tuneles intermedios
        x_mapa_destino = self.convertir_mazmorra_mapa(x) + direccion[0]
        y_mapa_destino = self.convertir_mazmorra_mapa(y) + direccion[1]
        x_destino = self.convertir_mapa_mazmorra(x_mapa_destino)
        y_destino = self.convertir_mapa_mazmorra(y_mapa_destino)
        while not(x == x_destino and y == y_destino):
            x += direccion[0]
            y += direccion[1]

            casilla = self.mazmorra[y][x]
            if casilla.esta_vacia():
                casilla.crear_tunel()
                self.celdas_ocupadas += 1

                if self.debug:
                    print(
                        "[DEBUG] Se crea el tunel ({0}, {1})".format(x, y))

        # Si la casilla destino era una habitacion en el mapa, crear habitacion
        casilla_destino = self.template.mapa[y_mapa_destino][x_mapa_destino]
        if casilla_destino.es_habitacion():
            self.crear_habitacion(x, y)

        # Si no se ha visitado esta casilla, pintar sus conexiones
        posicion_destino = (x_mapa_destino, y_mapa_destino)
        if posicion_destino not in casillas_visitadas:
            casillas_visitadas.add(posicion_destino)
            for giro in casilla_destino.conexiones:
                self.pintar_tunel_a_partir_de_mapa(
                    x, y, giro, casillas_visitadas)
        elif self.debug:
            print(
                "[DEBUG] Ya se ha visitado la casilla ({0}, {1})".format(x, y))

    def expandir_mazmorra(self):
        # Se da prioriedad a hacer las habitaciones mas grandes
        frecuencia_creacion_camino = int(1 / self.densidad_maxima)
        iteraciones_sin_crear_camino = 0

        celdas_totales = self.alto * self.ancho
        self.densidad = self.celdas_ocupadas / celdas_totales

        while self.densidad < self.densidad_maxima:
            # Expandir alguna habitacion
            indice = i_vegas.random_las_vegas(0, len(self.habitaciones))
            habitacion_aleatoria = list(self.habitaciones.values())[indice]
            self.ampliar_habitacion_aleatoriamente(habitacion_aleatoria)

            # Crear un nuevo camino
            if iteraciones_sin_crear_camino == frecuencia_creacion_camino:
                posicion_origen = self.encontrar_tunel_aleatorio()
                indice_direccion = i_vegas.random_las_vegas(
                    0, len(i_casilla.direcciones))
                direccion = i_casilla.direcciones[indice_direccion]
                self.crear_tunel(
                    posicion_origen[0], posicion_origen[1], direccion)
            else:
                iteraciones_sin_crear_camino += 1

            self.densidad = self.celdas_ocupadas / celdas_totales

    def ampliar_habitacion_aleatoriamente(self, habitacion):
        # Se intenta expandir en todas las direcciones disponibles hasta que se logra
        direcciones = list(i_casilla.direcciones.values())
        parar = False
        while not parar:
            # Obtener una direccion aleatoria de la lista y eliminarla
            indice_direccion = i_vegas.random_las_vegas(
                0, len(direcciones))
            direccion = direcciones[indice_direccion]
            del direcciones[indice_direccion]

            ampliada = self.ampliar_habitacion(
                habitacion, direccion)

            # Parar si se expandio o se agotaron las direcciones
            parar = ampliada or len(direcciones) == 0

    def ampliar_habitacion(self, habitacion, direccion):
        if self.debug:
            print("[DEBUG] Se va a intentar expandir la habitacion {0} en la direccion {1}".format(
                habitacion, direccion))

        # La direccion de ampliacion indica en que orden se crean las habitaciones durante la expansion
        # Si se expande a derecha o izquieda, las habitaciones se crearan de arriba a abajo
        # Si se expanda a arriba o abajo, las habitaciones se crearan de izquierda a derecha
        direccion_ampliacion = (
            abs(direccion[1]),
            abs(direccion[0])
        )

        posicion_partida = self.calcular_posicion_partida(
            habitacion, direccion)

        if not self.se_puede_expandir_en_direccion(posicion_partida, habitacion, direccion):
            return False

        es_inicial = habitacion.es_habitacion_inicial
        x = posicion_partida[0]
        y = posicion_partida[1]
        iteraciones = (habitacion.ancho) if direccion_ampliacion[0] != 0 else (
            habitacion.alto)

        for iteracion in range(iteraciones):
            casilla = self.mazmorra[y][x]
            if casilla.esta_vacia():
                self.celdas_ocupadas += 1

            casilla.crear_habitacion(es_inicial)

            if self.debug:
                print(
                    "[DEBUG] La posicion ({0}, {1}) pasa a ser una habitacion".format(x, y))

            x += direccion_ampliacion[0]
            y += direccion_ampliacion[1]

        # Si se ha movido a la izquierda o hacia arriba, actualizar posicion de la habitacion
        if direccion[0] == -1 or direccion[1] == -1:
            habitacion.posicion = (
                habitacion.posicion[0] + direccion[0], habitacion.posicion[1] + direccion[1])

        # Actualizar tamano de la habitacion
        if direccion[0] != 0:
            habitacion.ancho += 1
        else:
            habitacion.alto += 1

        return True

    def calcular_posicion_partida(self, habitacion, direccion):
        x = habitacion.posicion[0]
        y = habitacion.posicion[1]
        ancho = habitacion.ancho
        alto = habitacion.alto

        if direccion[0] == 0 and direccion[1] == -1:
            return (x, y - 1)
        elif direccion[0] == 1 and direccion[1] == 0:
            return (x + ancho, y)
        elif direccion[0] == 0 and direccion[1] == 1:
            return (x, y + alto)
        elif direccion[0] == -1 and direccion[1] == 0:
            return (x - 1, y)

    def se_puede_expandir_en_direccion(self, posicion_partida, habitacion, direccion):
        direccion_ampliacion = (
            abs(direccion[1]),
            abs(direccion[0])
        )

        # Dos iteraciones extra para comprobar las esquinas
        iteraciones = 2 + ((habitacion.ancho) if direccion_ampliacion[0] != 0 else (
            habitacion.alto))

        x = posicion_partida[0] - direccion_ampliacion[0]
        y = posicion_partida[1] - direccion_ampliacion[1]
        for iteracion in range(iteraciones):
            es_esquina = iteracion == 0 or iteracion == (iteraciones - 1)
            if not i_matriz_utils.pertenece_a_matriz((x, y), self.ancho, self.alto):
                if not es_esquina:
                    return False
                else:
                    continue

            casilla = self.mazmorra[y][x]
            if casilla.es_habitacion():
                return False

            # Para asegurar un espacio entre habitaciones
            if not i_matriz_utils.se_saldria_de_la_matriz((x, y), direccion, self.ancho, self.alto):
                x_siguiente = x + direccion[0]
                y_siguiente = y + direccion[1]
                celda_siguiente = self.mazmorra[y_siguiente][x_siguiente]

                if celda_siguiente.es_habitacion():
                    return False

            x += direccion_ampliacion[0]
            y += direccion_ampliacion[1]

        return True

    def encontrar_tunel_aleatorio(self):
        x = i_vegas.random_las_vegas(0, self.ancho)
        y = i_vegas.random_las_vegas(0, self.alto)

        while not self.mazmorra[y][x].es_tunel():
            x = i_vegas.random_las_vegas(0, self.ancho)
            y = i_vegas.random_las_vegas(0, self.alto)

        return (x, y)

    def crear_tunel(self, x0, y0, direccion):
        # Algoritmo muy similar al usado en TemplateMazmorra
        x = x0
        y = y0
        pasos_sin_girar = 0
        longitud_tunel = i_vegas.random_las_vegas(
            self.factor, self.template.l_max_tunel + self.factor)
        paso = 0

        if self.debug:
            print("[DEBUG] Se va a crear un tunel desde ({0}, {1}) en direccion {2} con longitud maxima {3}".format(
                x0, y0, direccion, longitud_tunel))

        continuar = True
        while continuar:
            # Girar si se sale de los limites
            if i_matriz_utils.se_saldria_de_la_matriz((x, y), direccion, self.ancho, self.alto):
                direccion = i_matriz_utils.calcular_nueva_direccion(
                    (x, y), direccion, self.ancho, self.alto)

                if self.debug:
                    print("[DEBUG] El tunel ha alcanzado los limites de la mazmorra. Nueva direccion {0}".format(
                        direccion))

            # Los giros son aleatorios en vez de predefinidos. Conforme avanza, mas probable es girar
            aleatorio = i_vegas.random_las_vegas(0, 100)
            probabilidad_giro = (1 - 1 / (0.15 * pasos_sin_girar + 1)) * 100
            if aleatorio < probabilidad_giro:
                direccion = i_matriz_utils.calcular_nueva_direccion(
                    (x, y), direccion, self.ancho, self.alto)
                pasos_sin_girar = 0

                if self.debug:
                    print(
                        "[DEBUG] El tunel gira en direccion {0}".format(direccion))
            else:
                pasos_sin_girar += 1

            # Avanzar
            x += direccion[0]
            y += direccion[1]
            casilla = self.mazmorra[y][x]

            # Crear tunel si es una casilla vacia. Detenerse si se encuentra una habitacion
            if casilla.esta_vacia():
                casilla.crear_tunel()
                self.celdas_ocupadas += 1

                if self.debug:
                    print(
                        "[DEBUG] Se crea un tunel en ({0}, {1})".format(x, y))
            elif casilla.es_habitacion():
                continuar = False

                if self.debug:
                    print(
                        "[DEBUG] El tunel ha alcanzado una habitacion en ({0}, {1}). Se termina de crear el tunel".format(x, y))

            paso += 1

            # Si este es el ultimo fragmento del tunel y no se ha encontrado habitacion, intentar crear una habitacion
            if paso > longitud_tunel and continuar:
                continuar = False

                x_habitacion = x + direccion[0]
                y_habitacion = y + direccion[1]

                if self.debug:
                    print("[DEBUG] El tunel ha alcanzado su longitud maxima. Se va a intentar crear una habitacion en ({0}, {1})".format(
                        x_habitacion, y_habitacion))

                self.intentar_crear_habitacion(x_habitacion, y_habitacion)

    def intentar_crear_habitacion(self, x0, y0):
        if not i_matriz_utils.pertenece_a_matriz((x0, y0), self.ancho, self.alto):
            if self.debug:
                print(
                    "[DEBUG] No se pudo crear la habitacion porque ({0}, {1}) se encuentra fuera de los limites de la mazmorra".format(x0, y0))

            return

        # Comprobar que no haya habitaciones alrededor
        x = x0 - 1
        x_final = x0 + 1
        while x <= x_final:
            y = y0 - 1
            y_final = y0 + 1
            while y <= y_final:
                if i_matriz_utils.pertenece_a_matriz((x, y), self.ancho, self.alto):
                    if self.mazmorra[y][x].es_habitacion():
                        if self.debug:
                            print(
                                "[DEBUG] Se ha encontrado una habitacion en ({0}, {1}). No se creara la habitacion".format(x, y))
                        return

                y += 1

            x += 1

        # Se crea la sala
        # Se tienen que falsificar para poder insertarlo en el diccionario
        x_mapa = self.ancho + x0
        y_mapa = self.alto + y0
        habitacion = i_habitacion.Habitacion((x0, y0), (x_mapa, y_mapa), False)
        self.habitaciones[(x_mapa, y_mapa)] = habitacion
        self.mazmorra[y0][x0].crear_habitacion()

        if self.debug:
            print(
                "[DEBUG] Se ha creado una habitacion en ({0}, {1}). Se va a intentar expandir".format(x0, y0))

        self.ampliar_habitacion_aleatoriamente(habitacion)

    def crear_tesoros(self):
        if self.debug:
            print("[DEBUG] Se van a instanciar tesoros")

        # Calcular tamaño medio de las habitaciones
        n_habitaciones = len(self.habitaciones)
        celdas_habitaciones = 0
        for habitacion in self.habitaciones.values():
            celdas = habitacion.ancho * habitacion.alto
            celdas_habitaciones += celdas

        media = celdas_habitaciones / n_habitaciones

        # Crear tesoros
        for habitacion in self.habitaciones.values():
            # Solo las habitaciones con tamano mayor o igual a la media son candidatas a alojar tesoros
            celdas = habitacion.ancho * habitacion.alto
            if celdas < media:
                continue

            # Aleatoriamente, decidir si aloja tesoro
            relacion = celdas / media * 100
            aleatorio = i_vegas.random_las_vegas(0, 100)
            if aleatorio < (relacion - 100):
                self.crear_tesoro(habitacion)

    def crear_tesoro(self, habitacion):
        # Escoger un tesoror entre las colecciones de tesoros disponibles
        indice_aleatorio = i_vegas.random_las_vegas(0, len(self.lista_tesoros))
        tesoros = self.lista_tesoros[indice_aleatorio]
        tesoro = tesoros.obtener_tesoro_aleatorio()

        # Crear tesoro
        posicion_tesoro = habitacion.posicion_aleatoria()
        x = posicion_tesoro[0]
        y = posicion_tesoro[1]
        casilla = self.mazmorra[y][x]
        casilla.crear_tesoro(tesoro)

        if self.debug:
            print("[DEBUG] Se crea el tesoro {0} en {1}".format(
                tesoro, posicion_tesoro))

    def crear_habitacion(self, x, y, inicial=False):
        x_mapa = self.convertir_mazmorra_mapa(x)
        y_mapa = self.convertir_mazmorra_mapa(y)

        habitacion = i_habitacion.Habitacion((x, y), (x_mapa, y_mapa), inicial)
        if habitacion in self.habitaciones:
            if self.debug:
                print(
                    "[DEBUG] La habitacion en ({0}, {1}) ya se ha visitado".format(x, y))

            return

        self.habitaciones[(x_mapa, y_mapa)] = habitacion

        casilla = i_casilla.Casilla((x, y))
        casilla.crear_habitacion(inicial)
        self.mazmorra[y][x] = casilla

        if self.debug:
            print("[DEBUG] Se visita la habitacion ({0}, {1})".format(x, y))

    def convertir_mazmorra_mapa(self, coordenada):
        return coordenada // self.factor

    def convertir_mapa_mazmorra(self, coordenada):
        factor_medios = self.factor >> 1
        return coordenada * self.factor + factor_medios

    def imprimir_mazmorra(self):
        for fila in self.mazmorra:
            for casilla in fila:
                print(casilla, " ", end="")
            print("")

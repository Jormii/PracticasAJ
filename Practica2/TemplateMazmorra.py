import importlib

i_casilla = importlib.import_module("Casilla")
i_vegas = importlib.import_module("LasVegas")
i_matriz_utils = importlib.import_module("MatrizUtils")


class TemplateMazmorra(object):
    def __init__(self, ancho, alto, n_tuneles, l_max_tunel, debug=False):
        self.ancho = ancho
        self.alto = alto
        self.n_tuneles = n_tuneles
        self.l_max_tunel = l_max_tunel
        self.debug = debug

        self.casilla_inicial = None
        self.mapa = []

    def random_walk(self):
        self.crear_mapa()
        x0, y0 = self.obtener_posicion_inicial()

        # Crear tuneles y habitaciones
        for t in range(self.n_tuneles):
            x, y, direccion, se_encontro_habitacion = self.crear_tunel(x0, y0)
            if not se_encontro_habitacion:
                self.crear_habitacion(x, y, direccion)

        # Calcular conexiones entre tuneles y habitaciones
        for fila in self.mapa:
            for casilla in fila:
                casilla.calcular_conexiones(self.mapa, self.ancho, self.alto)

        return self.mapa

    def crear_mapa(self):
        self.mapa.clear()
        for y in range(self.alto):
            self.mapa.append([0] * self.ancho)
            for x in range(self.ancho):
                posicion = (x, y)
                self.mapa[y][x] = i_casilla.Casilla(posicion)

        if self.debug:
            print("[DEBUG:TemplateMazmorra]")
            print("[DEBUG] Creando mapa de {0}x{1}".format(
                self.ancho, self.alto))

    def obtener_posicion_inicial(self):
        x0 = i_vegas.random_las_vegas(0, self.ancho)
        y0 = i_vegas.random_las_vegas(0, self.alto)

        self.casilla_inicial = self.mapa[y0][x0]
        self.casilla_inicial.crear_habitacion(True)

        if self.debug:
            print("[DEBUG] Posicion inicial ({0}, {1})".format(x0, y0))

        return x0, y0

    def crear_tunel(self, x0, y0):
        # Inicializar variables
        longitud = i_vegas.random_las_vegas(1, self.l_max_tunel + 1)
        punto_giro = i_vegas.random_las_vegas(1, longitud + 1)

        indice_aleatorio = i_vegas.random_las_vegas(
            0, len(i_casilla.direcciones))
        direccion_aleatoria = i_casilla.direcciones[indice_aleatorio]
        direccion = i_matriz_utils.calcular_nueva_direccion(
            (x0, y0), direccion_aleatoria, self.ancho, self.alto)

        if self.debug:
            print("[DEBUG] Pintando nuevo tunel")
            print("[DEBUG] Longitud del tunel: {0}".format(longitud))
            print(
                "[DEBUG] Punto de giro del tunel: {0}".format(punto_giro))
            print("[DEBUG] Direccion del tunel: {0}".format(direccion))

        x = x0
        y = y0
        paso = 1
        for paso in range(0, longitud):
            # En caso de que se alcance el punto de giro
            if paso == punto_giro:
                direccion = i_matriz_utils.calcular_nueva_direccion(
                    (x, y), direccion, self.ancho, self.alto)

                if self.debug:
                    print("[DEBUG] Se ha alcanzado el punto de giro. Nueva direccion: {0}".format(
                        direccion))

            # Si se han alcanzado los limites del mapa
            if i_matriz_utils.se_saldria_de_la_matriz((x, y), direccion, self.ancho, self.alto):
                direccion = i_matriz_utils.calcular_nueva_direccion(
                    (x, y), direccion, self.ancho, self.alto)

                if self.debug:
                    print("[DEBUG] El tunel ha alcanzado una pared. Nueva direccion: {0}".format(
                        direccion))

            # Intentar crear tunel
            x += direccion[0]
            y += direccion[1]
            casilla = self.mapa[y][x]

            # Si se ha alcanzado una habitacion se deja de crear el camino
            if casilla.es_habitacion():
                if self.debug:
                    print(
                        "[DEBUG] Se ha encontrado una habitacion en ({0}, {1}). Terminando iteracion".format(x, y))

                return x, y, direccion, True

            casilla.crear_tunel()

            if self.debug:
                print(
                    "[DEBUG] Se ha pintado un tunel en ({0}, {1})".format(x, y))

            paso += 1

        return x, y, direccion, False

    def crear_habitacion(self, x, y, direccion):
        if i_matriz_utils.se_saldria_de_la_matriz((x, y), direccion, self.ancho, self.alto):
            direccion = i_matriz_utils.calcular_nueva_direccion(
                (x, y), direccion, ancho, alto)

            if self.debug:
                print("[DEBUG] Se crearia una habitacion fuera de los limites del mapa. Nueva direccion {0}".format(
                    direccion))

        x += direccion[0]
        y += direccion[1]
        casilla = self.mapa[y][x]
        if not casilla.es_tunel():
            casilla.crear_habitacion()

            if self.debug:
                print(
                    "[DEBUG] Se ha creado una habitacion en ({0}, {1})".format(x, y))
        elif self.debug:
            print(
                "[DEBUG] No se ha creado una habitacion porque hay un tunel en ({0}, {1})".format(x, y))

    def imprimir_mapa(self, esconder_vacias=True):
        for fila in self.mapa:
            for casilla in fila:
                print(" " if casilla.tipo ==
                      i_casilla.vacio and esconder_vacias else casilla.tipo, " ", end="")
            print("")

    def imprimir_mapa_detalle(self):
        for fila in self.mapa:
            for casilla in fila:
                print(casilla, " ", end="")
            print("")

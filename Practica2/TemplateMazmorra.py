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
        self.mapa = []  # Matriz de referencia que se utilizara para generar la mazmorra

    # Genera el mapa utilizando random walk
    def random_walk(self):
        self.inicializar_mapa()
        x0, y0 = self.obtener_posicion_inicial()

        # Crear tuneles y habitaciones
        for t in range(self.n_tuneles):
            x, y, direccion, se_encontro_habitacion = self.crear_tunel(x0, y0)
            if not se_encontro_habitacion:
                self.crear_habitacion(x, y, direccion)

        return self.mapa

    def inicializar_mapa(self):
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
        self.casilla_inicial.crear_habitacion(inicial=True)

        if self.debug:
            print("[DEBUG] Posicion inicial ({0}, {1})".format(x0, y0))

        return x0, y0

    # Crear tunel crea un tunel aleatorio. Devuelve donde termino el tunel, en que direccion y se al final se encontro una habitacion
    def crear_tunel(self, x0, y0):
        longitud, punto_giro, direccion = self.inicializar_variables_tunel(
            x0, y0)

        x = x0
        y = y0
        for paso in range(0, longitud):
            # En caso de que se alcance el punto de giro o se alcanzaran los limites del mapa con el siguiente movimiento
            if paso == punto_giro or i_matriz_utils.se_saldria_de_la_matriz((x, y), direccion, self.ancho, self.alto):
                direccion = i_matriz_utils.calcular_nueva_direccion(
                    (x, y), direccion, self.ancho, self.alto)

                if self.debug:
                    print("[DEBUG] Se ha alcanzado el punto de giro. Nueva direccion: {0}".format(
                        direccion))

            # Crear conexion en la casilla previa
            casilla_previa = self.mapa[y][x]
            casilla_previa.anadir_conexion(direccion)

            # Avanzar
            x += direccion[0]
            y += direccion[1]
            casilla = self.mapa[y][x]

            # Si se ha alcanzado una habitacion se deja de crear el tunel
            if casilla.es_habitacion():
                if self.debug:
                    print(
                        "[DEBUG] Se ha encontrado una habitacion en ({0}, {1}). Terminando iteracion".format(x, y))

                return x, y, direccion, True
            else:
                casilla.crear_tunel()

                if self.debug:
                    print(
                        "[DEBUG] Se ha pintado un tunel en ({0}, {1})".format(x, y))

        return x, y, direccion, False

    def inicializar_variables_tunel(self, x0, y0):
        longitud = i_vegas.random_las_vegas(1, self.l_max_tunel + 1)
        punto_giro = i_vegas.random_las_vegas(1, longitud + 1)

        indice_aleatorio = i_vegas.random_las_vegas(
            0, len(i_casilla.direcciones))
        direccion_aleatoria = i_casilla.direcciones[indice_aleatorio]

        # Se calcula una nueva direccion puesto que existe la posibilidad de que la aleatoria apuntara a los bordes del mapa
        direccion = i_matriz_utils.calcular_nueva_direccion(
            (x0, y0), direccion_aleatoria, self.ancho, self.alto)

        if self.debug:
            print("[DEBUG] Pintando nuevo tunel")
            print("[DEBUG] Longitud del tunel: {0}".format(longitud))
            print("[DEBUG] Punto de giro del tunel: {0}".format(punto_giro))
            print("[DEBUG] Direccion del tunel: {0}".format(direccion))

        return longitud, punto_giro, direccion

    def crear_habitacion(self, x, y, direccion):
        # Girar en caso de que la siguiente posicion no pertenezca al mapa
        if i_matriz_utils.se_saldria_de_la_matriz((x, y), direccion, self.ancho, self.alto):
            direccion = i_matriz_utils.calcular_nueva_direccion(
                (x, y), direccion, self.ancho, self.alto)

            if self.debug:
                print("[DEBUG] Se crearia una habitacion fuera de los limites del mapa. Nueva direccion {0}".format(
                    direccion))

        # Crear conexion en la casilla previa
        casilla_previa = self.mapa[y][x]
        casilla_previa.anadir_conexion(direccion)

        # Avanzar
        x += direccion[0]
        y += direccion[1]
        casilla = self.mapa[y][x]

        # No se crea habitacion a menos que este vacia
        if casilla.esta_vacia():
            casilla.crear_habitacion()

            if self.debug:
                print(
                    "[DEBUG] Se ha creado una habitacion en ({0}, {1})".format(x, y))
        elif self.debug:
            print(
                "[DEBUG] No se ha creado una habitacion. Ya existia algo en ({0}, {1})".format(x, y))

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

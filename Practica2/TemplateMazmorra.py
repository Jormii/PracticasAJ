import random  # TODO: Aleatorios vistos en clase
import importlib

c = importlib.import_module("Casilla")

direcciones = {
    0: (0, -1),    # Norte
    1: (1, 0),     # Este
    2: (0, 1),     # Sur
    3: (-1, 0)     # Oeste
}


class TemplateMazmorra(object):
    def __init__(self, ancho, alto, n_tuneles, l_max_tunel, debug=False):
        self.ancho = ancho
        self.alto = alto
        self.n_tuneles = n_tuneles
        self.l_max_tunel = l_max_tunel
        self.debug = debug

        self.casilla_inicial = None
        self.posicion_inicial = None
        self.mapa = []

    def random_walk(self):
        # Crear mapa y limpiar habitaciones
        self.mapa = []
        for i in range(self.alto):
            self.mapa.append([0] * self.ancho)
            for j in range(self.ancho):
                self.mapa[i][j] = c.Casilla()

        if self.debug:
            print("[DEBUG:TemplateMazmorra]")
            print("[DEBUG] Creando mapa de {0}x{1}".format(
                self.ancho, self.alto))

        # Calcular posicion inicial
        random.seed(None)
        x0 = random.randint(0, self.ancho - 1)
        y0 = random.randint(0, self.alto - 1)

        self.casilla_inicial = self.mapa[y0][x0]
        self.casilla_inicial.tipo = c.habitacion
        self.posicion_inicial = (x0, y0)

        if self.debug:
            print("[DEBUG] Posicion inicial ({0}, {1})".format(x0, y0))

        # Crear tuneles y salas
        for t in range(self.n_tuneles):
            x, y, direccion, se_encontro_sala = self.crear_tunel(x0, y0, t)
            if not se_encontro_sala:
                self.crear_sala(x, y, direccion)

        # Devolver mapa y casilla inicial
        return self.mapa, self.casilla_inicial

    def crear_tunel(self, x0, y0, t):
        longitud = random.randint(1, self.l_max_tunel)
        punto_giro = random.randint(1, longitud)
        direccion_aleatoria = direcciones[random.randint(0, 3)]
        direccion = self.calcular_nueva_direccion(x0, y0, direccion_aleatoria)
        
        self.casilla_inicial.anadir_giro(direccion)

        if self.debug:
            print("[DEBUG] Pintando tunel numero {0}".format(t + 1))
            print("[DEBUG] Longitud del tunel: {0}".format(longitud))
            print(
                "[DEBUG] Punto de giro del tunel: {0}".format(punto_giro))
            print("[DEBUG] Direccion del tunel: {0}".format(direccion))

        x = x0
        y = y0
        paso = 1
        for paso in range(0, longitud):
            if paso == punto_giro:
                direccion = self.calcular_nueva_direccion(
                    x, y, direccion)

                casilla = self.mapa[y][x]
                casilla.anadir_giro(direccion)

                if self.debug:
                    print("[DEBUG] Se ha alcanzado el punto de giro. Nueva direccion: {0}".format(
                        direccion))

            if self.se_saldria_del_mapa(x, y, direccion):
                direccion = self.calcular_nueva_direccion(
                    x, y, direccion)

                casilla = self.mapa[y][x]
                casilla.anadir_giro(direccion)

                if self.debug:
                    print("[DEBUG] El tunel ha alcanzado una pared. Nueva direccion: {0}".format(
                        direccion))

            x += direccion[0]
            y += direccion[1]
            casilla = self.mapa[y][x]
            if casilla.tipo == c.habitacion:
                if self.debug:
                    print(
                        "[DEBUG] Se ha encontrado una habitacion en ({0}, {1}). Terminando iteracion".format(x, y))

                return x, y, direccion, True

            casilla.tipo = c.tunel

            if self.debug:
                print(
                    "[DEBUG] Se ha pintado un tunel en ({0}, {1})".format(x, y))

            paso += 1

        return x, y, direccion, False

    def crear_sala(self, x, y, direccion):
        # Crear sala
        if self.se_saldria_del_mapa(x, y, direccion):
            direccion = self.calcular_nueva_direccion(x, y, direccion)

            casilla = self.mapa[y][x]
            casilla.anadir_giro(direccion)

            if self.debug:
                print("[DEBUG] Se crearia una sala fuera de los limites del mapa. Nueva direccion {0}".format(
                    direccion))

        x += direccion[0]
        y += direccion[1]
        casilla = self.mapa[y][x]
        if casilla.tipo != c.tunel:
            casilla.tipo = c.habitacion

            if self.debug:
                print(
                    "[DEBUG] Se ha creado una sala en ({0}, {1})".format(x, y))
        elif self.debug:
            print(
                "[DEBUG] No se ha creado sala porque hay un tunel en ({0}, {1})".format(x, y))

    def se_saldria_del_mapa(self, x, y, direccion):
        x += direccion[0]
        y += direccion[1]

        return x < 0 or y < 0 or x >= self.ancho or y >= self.alto

    def calcular_nueva_direccion(self, x, y, direccion):
        # TODO: En las esquinas a veces produce giros hacia la pared

        # Se mueve hacia el norte o sur
        if direccion[0] == 0:
            # %x € [0, 1], si extremo izquierdo/derecho
            porcentaje_en_x = x / (self.ancho - 1)
            girar_derecha = random.random() > porcentaje_en_x
            nueva_direccion = direcciones[1] if girar_derecha else direcciones[3]
        # Se mueve hacia el oeste o este
        else:
            # %y € [0, 1], si extremo superior/inferior
            porcentaje_en_y = y / (self.alto - 1)
            girar_abajo = random.random() > porcentaje_en_y
            nueva_direccion = direcciones[2] if girar_abajo else direcciones[0]

        return nueva_direccion

    def imprimir_mapa(self):
        for fila in self.mapa:
            for casilla in fila:
                print(casilla.tipo, " ", end="")
            print("")
            
    def imprimir_mapa_detalle(self):
        for fila in self.mapa:
            for casilla in fila:
                print(casilla, " ", end="")
            print("")

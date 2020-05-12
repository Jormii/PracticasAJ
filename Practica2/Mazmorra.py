import importlib

c = importlib.import_module("Casilla")
t = importlib.import_module("TemplateMazmorra")


class Mazmorra(object):
    def __init__(self, template, factor, densidad_maxima, debug=False):
        self.template = template
        self.factor = factor
        self.densidad_maxima = densidad_maxima
        self.debug = debug

        self.mazmorra = []
        self.casillas_visitadas = set()
        self.habitaciones = []
        self.celdas_ocupadas = 0
        self.densidad = 0

    def generar_mazmorra(self):
        # Reiniciar variables
        self.habitaciones.clear()
        self.celdas_ocupadas = 0
        
        # Generar mazmorra
        alto = self.template.alto * self.factor
        ancho = self.template.ancho * self.factor
        for i in range(alto):
            self.mazmorra.append([0] * ancho)

        # En caso de que se llame antes a generar_mazmorra
        if not self.template.casilla_inicial:
            self.template.random_walk()

        casilla_inicial = self.template.casilla_inicial

        posicion_inicial_mapa = self.template.posicion_inicial
        x0 = self.convertir_mapa_mazmorra(posicion_inicial_mapa[0])
        y0 = self.convertir_mapa_mazmorra(posicion_inicial_mapa[1])

        self.habitaciones

        if self.debug:
            print("[DEBUG:Mazmorra]")
            print(
                "[DEBUG] Creando mazmorra a partir de la posicion ({0}, {1})".format(x0, y0))

        self.casillas_visitadas.clear()
        self.casillas_visitadas.add(posicion_inicial_mapa)
        self.anadir_habitacion(x0, y0)

        for direccion in casilla_inicial.conexiones:
            self.pintar_tunel(x0, y0, direccion)

        celdas_totales = alto * ancho
        self.densidad = self.celdas_ocupadas / celdas_totales
        while self.densidad < self.densidad_maxima:
            # TODO
            break

        return self.mazmorra

    def pintar_tunel(self, x, y, direccion):
        if self.debug:
            print("[DEBUG] Pintando tunel desde ({0}, {1}) en direccion {2}".format(
                x, y, direccion))

        x_mapa_destino = self.convertir_mazmorra_mapa(x) + direccion[0]
        y_mapa_destino = self.convertir_mazmorra_mapa(y) + direccion[1]
        x_destino = self.convertir_mapa_mazmorra(x_mapa_destino)
        y_destino = self.convertir_mapa_mazmorra(y_mapa_destino)
        while not(x == x_destino and y == y_destino):
            x += direccion[0]
            y += direccion[1]

            self.mazmorra[y][x] = c.tunel
            self.celdas_ocupadas += 1

        casilla_destino = self.template.mapa[y_mapa_destino][x_mapa_destino]
        if casilla_destino.tipo == c.habitacion:
            self.anadir_habitacion(x, y)

        posicion_destino = (x_mapa_destino, y_mapa_destino)
        if posicion_destino not in self.casillas_visitadas:
            self.casillas_visitadas.add(posicion_destino)
            for giro in casilla_destino.conexiones:
                self.pintar_tunel(x, y, giro)
        elif self.debug:
            print(
                "[DEBUG] Ya se ha visitado la casilla ({0}, {1})".format(x, y))

    def anadir_habitacion(self, x, y):
        x_mapa = self.convertir_mazmorra_mapa(x)
        y_mapa = self.convertir_mazmorra_mapa(y)
        
        entrada = ((x, y), (x_mapa, y_mapa))
        if entrada in self.habitaciones:
            return False
        
        self.mazmorra[y][x] = c.habitacion
        self.habitaciones.append(entrada)
        return True

    def convertir_mazmorra_mapa(self, coordenada):
        return coordenada // self.factor

    def convertir_mapa_mazmorra(self, coordenada):
        factor_medios = self.factor >> 1
        return coordenada * self.factor + factor_medios

    def imprimir_mazmorra(self, esconder_vacias=True):
        for fila in self.mazmorra:
            for casilla in fila:
                print(" " if casilla ==
                      c.vacio and esconder_vacias else casilla, " ", end="")
            print("")

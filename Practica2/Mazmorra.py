import importlib

c = importlib.import_module("Casilla")
t = importlib.import_module("TemplateMazmorra")


class Mazmorra(object):
    def __init__(self, template, factor, debug=False):
        self.template = template
        self.factor = factor
        self.debug = debug

        self.mazmorra = []

    def generar_mazmorra(self):
        # Generar mazmorra
        alto = self.template.alto * self.factor
        ancho = self.template.ancho * self.factor
        for i in range(alto):
            self.mazmorra.append([0] * ancho)

        casilla_inicial = self.template.casilla_inicial

        posicion_inicial_mapa = self.template.posicion_inicial
        x0 = self.convertir_mapa_mazmorra(posicion_inicial_mapa[0])
        y0 = self.convertir_mapa_mazmorra(posicion_inicial_mapa[1])

        self.mazmorra[y0][x0] = c.habitacion
        for direccion in casilla_inicial.giros:
            self.pintar_tunel(x0, y0, direccion)

        return self.mazmorra

    def pintar_tunel(self, x, y, direccion):
        continuar = True
        x_mapa_destino = self.convertir_mazmorra_mapa(x) + direccion[0]
        y_mapa_destino = self.convertir_mazmorra_mapa(y) + direccion[1]
        x_destino = self.convertir_mapa_mazmorra(x_mapa_destino)
        y_destino = self.convertir_mapa_mazmorra(y_mapa_destino)
        while not(x == x_destino and y == y_destino):
            x += direccion[0]
            y += direccion[1]

            self.mazmorra[y][x] = c.tunel

        casilla_destino = self.template.mapa[y_mapa_destino][x_mapa_destino]
        if casilla_destino.tipo == c.habitacion:
            self.mazmorra[y][x] = c.habitacion
            
        for giro in casilla_destino.giros:
            self.pintar_tunel(x, y, giro)

    def convertir_mazmorra_mapa(self, coordenada):
        return coordenada // self.factor

    def convertir_mapa_mazmorra(self, coordenada):
        factor_medios = self.factor >> 1
        return coordenada * self.factor + factor_medios

    def imprimir_mazmorra(self):
        for fila in self.mazmorra:
            for columna in fila:
                print(columna, " ", end="")
            print("")

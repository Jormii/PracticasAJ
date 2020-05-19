from enum import Enum
import importlib

direcciones = {
    0: (0, -1),    # Norte
    1: (1, 0),     # Este
    2: (0, 1),     # Sur
    3: (-1, 0)     # Oeste
}

orientaciones = {
    (0, -1): 0,
    (1, 0): 1,
    (0, 1): 2,
    (-1, 0): 3
}


class TiposCasilla(Enum):
    VACIA = 0
    TUNEL = 1
    HABITACION = 2
    TESORO = 3


i_template = importlib.import_module("TemplateMazmorra")
i_matriz_utils = importlib.import_module("MatrizUtils")


class Casilla(object):
    def __init__(self, posicion):
        self.posicion = posicion
        self.tipo = TiposCasilla.VACIA
        self.es_casilla_inicial = False
        self.conexiones = set()
        self.tesoro = None

    def crear_tunel(self):
        self.tipo = TiposCasilla.TUNEL

    def crear_habitacion(self, inicial=False):
        self.tipo = TiposCasilla.HABITACION
        self.es_casilla_inicial = inicial

    def crear_tesoro(self, tesoro):
        self.tipo = TiposCasilla.TESORO
        self.tesoro = tesoro

    def anadir_conexion(self, direccion):
        self.conexiones.add(direccion)

    def calcular_conexiones(self, matriz, ancho, alto):
        if self.tipo == TiposCasilla.VACIA:
            return

        x0 = self.posicion[0]
        y0 = self.posicion[1]
        for direccion in direcciones.values():
            x = x0 + direccion[0]
            y = y0 + direccion[1]

            if not i_matriz_utils.pertenece_a_matriz((x, y), ancho, alto):
                continue

            casilla = matriz[y][x]
            if casilla.tipo != TiposCasilla.VACIA:
                self.conexiones.add(direccion)

    def orientacion(self):
        orientacion_media = 0
        for conexion in self.conexiones:
            orientacion = orientaciones[conexion]
            orientacion_media += orientacion

        return orientacion_media / len(self.conexiones)

    def esta_vacia(self):
        return self.tipo == TiposCasilla.VACIA

    def es_tunel(self):
        return self.tipo == TiposCasilla.TUNEL

    def es_habitacion(self):
        return self.tipo == TiposCasilla.HABITACION or self.tipo == TiposCasilla.TESORO

    def almacena_tesoro(self):
        return self.tipo == TiposCasilla.TESORO

    def __repr__(self):
        if self.tipo == TiposCasilla.VACIA:
            return "[0]"

        g = self.conexiones if len(self.conexiones) != 0 else "[]"
        return "[{0}, {1}]".format(self.tipo.value, g)

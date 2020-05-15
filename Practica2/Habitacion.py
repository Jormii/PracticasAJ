class Habitacion(object):
    def __init__(self, posicion, posicion_mapa, es_habitacion_inicial):
        self.posicion = posicion
        self.posicion_mapa = posicion_mapa
        self.ancho = 1
        self.alto = 1
        self.es_habitacion_inicial = es_habitacion_inicial

    def __hash__(self):
        return self.posicion_mapa.__hash__()

    def __repr__(self):
        return "{0}, {1}, {2}x{3}".format(self.posicion, self.posicion_mapa, self.ancho, self.alto)

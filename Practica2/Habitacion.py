class Habitacion(object):
    def __init__(self, posicion, posicion_mapa, es_habitacion_inicial):
        self.posicion = posicion
        self.posicion_mapa = posicion_mapa
        self.ancho = 1
        self.alto = 1
        self.es_habitacion_inicial = es_habitacion_inicial

    def casilla_en_habitacion(self, x, y):
        ancho_fin = self.posicion[0] + self.ancho
        alto_fin = self.posicion[1] + self.alto
        return x >= self.posicion[0] and x < ancho_fin and y >= self.posicion[1] and y < alto_fin

    def __hash__(self):
        return self.posicion_mapa.__hash__()

    def __repr__(self):
        return "{0}, {1}, {2}x{3}".format(self.posicion, self.posicion_mapa, self.ancho, self.alto)

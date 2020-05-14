vacio = 0
tunel = 1
habitacion = 2


class Casilla(object):
    def __init__(self):
        self.tipo = vacio
        self.es_casilla_inicial = False
        self.conexiones = set()

    def anadir_conexion(self, direccion):
        self.conexiones.add(direccion)

    def __repr__(self):
        if self.tipo == vacio:
            return "[0]"

        g = self.conexiones if len(self.conexiones) != 0 else "[]"
        return "[{0}, {1}]".format(self.tipo, g)

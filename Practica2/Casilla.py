vacio = 0
tunel = 1
habitacion = 2


class Casilla(object):
    def __init__(self):
        self.tipo = vacio
        self.giros = set()

    def anadir_giro(self, direccion):
        self.giros.add(direccion)

    def __repr__(self):
        if self.tipo == vacio:
            return "[0]"
        
        g = self.giros if len(self.giros) != 0 else "[]"
        return "[{0}, {1}]".format(self.tipo, g)
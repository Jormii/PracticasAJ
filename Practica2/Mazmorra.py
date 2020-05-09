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
        x0 = self.template.posicion_inicial[0] + self.factor >> 1
        y0 = self.template.posicion_inicial[1] + self.factor >> 1
        
        self.mazmorra[y0][x0] = "*"
        for direccion in casilla_inicial.giros:
            self.pintar_tunel(x0, y0, direccion)

        return self.mazmorra

    def pintar_tunel(self, x, y, direccion):
        continuar = True
        while continuar:
            x += direccion[0]
            y += direccion[1]
            
            x_mapa = x // self.factor
            y_mapa = y // self.factor
            
            casilla = self.template.mapa[y_mapa][x_mapa]
            if casilla.tipo == c.habitacion:
                self.mazmorra[y][x] = c.habitacion    
                continuar = False
            else:
                self.mazmorra[y][x] = c.tunel
                for nueva_direccion in casilla.giros:
                    self.pintar_tunel(x, y, nueva_direccion)
            
    def imprimir_mazmorra(self):
        for fila in self.mazmorra:
            for columna in fila:
                print(columna, " ", end="")
            print("")

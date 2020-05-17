import importlib

i_dfd = importlib.import_module("DiscreteFiniteDistribution")


class Tesoro(object):
    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return self.nombre


class Tesoros(object):
    def __init__(self, tuplas_peso_tesoro):
        self.tesoros = []
        self.pesos = []

        pesos_totales = 0
        for tupla in tuplas_peso_tesoro:
            pesos_totales += tupla[0]

        for tupla in tuplas_peso_tesoro:
            peso = int(tupla[0] / pesos_totales * 100)
            tesoro = tupla[1]

            self.pesos.append(peso)
            self.tesoros.append(tesoro)

    def obtener_tesoro(self):
        indice = i_dfd.random_from_weights(self.pesos)
        return self.tesoros[indice]

    def __repr__(self):
        return (self.tesoros, self.pesos)

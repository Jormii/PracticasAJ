class Tesoros(object):
    def __init__(self, tuplas_tesoros):
        self.tesoros = []
        
        pesos_totales = 0
        for tupla in tuplas_tesoros:
            pesos_totales += tupla[1]
            
        for tupla in tuplas_tesoros:
            e = tupla[0]
            peso = tupla[1] / pesos_totales
            self.tesoros.append((e, peso))
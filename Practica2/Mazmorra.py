import importlib
import random  # TODO: Metodos vistos en clase

i_casilla = importlib.import_module("Casilla")
i_template = importlib.import_module("TemplateMazmorra")
i_habitacion = importlib.import_module("Habitacion")


class Mazmorra(object):
    def __init__(self, template, factor, densidad_maxima, debug=False):
        self.template = template
        self.factor = factor
        self.densidad_maxima = densidad_maxima
        self.debug = debug

        self.ancho = template.ancho * factor
        self.alto = template.alto * factor
        self.mazmorra = []
        self.casillas_visitadas = set()
        self.habitaciones = {}
        self.celdas_ocupadas = 0
        self.densidad = 0

    def generar_mazmorra(self):
        random.seed(None)

        # Reiniciar variables
        self.mazmorra.clear()
        self.habitaciones.clear()
        self.celdas_ocupadas = 1    # Casilla inicial

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

        if self.debug:
            print("[DEBUG:Mazmorra]")
            print(
                "[DEBUG] Creando mazmorra a partir de la posicion ({0}, {1})".format(x0, y0))

        self.casillas_visitadas.clear()
        self.casillas_visitadas.add(posicion_inicial_mapa)
        self.anadir_habitacion(x0, y0, True)

        for direccion in casilla_inicial.conexiones:
            self.pintar_tunel(x0, y0, direccion)

        for habitacion in self.habitaciones.values():
            self.ampliar_habitacion(habitacion)

        celdas_totales = alto * ancho
        self.densidad = self.celdas_ocupadas / celdas_totales
        habitaciones_a_ampliar = list(self.habitaciones.values())
        while self.densidad < self.densidad_maxima and len(habitaciones_a_ampliar) != 0:
            habitacion_aleatoria = random.choice(habitaciones_a_ampliar)
            ampliada = self.ampliar_habitacion(habitacion_aleatoria)
            if not ampliada:
                habitaciones_a_ampliar.remove(habitacion)
                
            self.densidad = self.celdas_ocupadas / celdas_totales

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

            if self.mazmorra[y][x] == i_casilla.vacio:
                self.mazmorra[y][x] = i_casilla.tunel
                self.celdas_ocupadas += 1

                if self.debug:
                    print("[DEBUG] Se pinta la celda ({0}, {1})".format(x, y))

        casilla_destino = self.template.mapa[y_mapa_destino][x_mapa_destino]
        if casilla_destino.tipo == i_casilla.habitacion:
            self.anadir_habitacion(x, y)

        posicion_destino = (x_mapa_destino, y_mapa_destino)
        if posicion_destino not in self.casillas_visitadas:
            self.casillas_visitadas.add(posicion_destino)
            for giro in casilla_destino.conexiones:
                self.pintar_tunel(x, y, giro)
        elif self.debug:
            print(
                "[DEBUG] Ya se ha visitado la casilla ({0}, {1})".format(x, y))

    def ampliar_habitacion(self, habitacion):
        relacion_ancho_alto = habitacion.ancho / habitacion.alto
        aleatorio = random.random()
        signo = 1 if random.random() > 0.5 else -1
        if aleatorio * relacion_ancho_alto > 0.5:
            direccion = (0, signo)
            direccion_ampliacion = (1, 0)
        else:
            direccion = (signo, 0)
            direccion_ampliacion = (0, 1)

        if self.debug:
            print("[DEBUG] Se va a expandir la habitacion {0} en la direccion {1}".format(
                habitacion, direccion))

        # TODO: Añadir comprobacion para que no se salga de los limites
        posicion_partida = self.calcular_posicion_partida(
            habitacion, direccion)
        x = posicion_partida[0]
        y = posicion_partida[1]
        iteraciones = (habitacion.ancho) if direccion_ampliacion[0] != 0 else (
            habitacion.alto)
        for iteracion in range(iteraciones):
            if self.mazmorra[y][x] == i_casilla.vacio:
                self.celdas_ocupadas += 1

            self.mazmorra[y][x] = i_casilla.habitacion if not habitacion.es_habitacion_inicial else i_casilla.inicial

            if self.debug:
                print(
                    "[DEBUG] La posicion ({0}, {1}) pasa a ser una habitacion".format(x, y))

            x += direccion_ampliacion[0]
            y += direccion_ampliacion[1]

        # Actualizar posicion de la habitacion
        if direccion[0] == -1 or direccion[1] == -1:
            habitacion.posicion = (
                habitacion.posicion[0] + direccion[0], habitacion.posicion[1] + direccion[1])

        # Actualizar tamano de la habitacion
        if direccion[0] != 0:
            habitacion.ancho += 1
        else:
            habitacion.alto += 1

        return True

    def calcular_posicion_partida(self, habitacion, direccion):
        x = habitacion.posicion[0]
        y = habitacion.posicion[1]
        ancho = habitacion.ancho
        alto = habitacion.alto

        if direccion[0] == 0 and direccion[1] == -1:
            return (x, y - 1)
        elif direccion[0] == 1 and direccion[1] == 0:
            return (x + ancho, y)
        elif direccion[0] == 0 and direccion[1] == 1:
            return (x, y + alto)
        elif direccion[0] == -1 and direccion[1] == 0:
            return (x - 1, y)

    def anadir_habitacion(self, x, y, inicial=False):
        x_mapa = self.convertir_mazmorra_mapa(x)
        y_mapa = self.convertir_mazmorra_mapa(y)

        habitacion = i_habitacion.Habitacion((x, y), (x_mapa, y_mapa), inicial)
        if habitacion in self.habitaciones:
            if self.debug:
                print(
                    "[DEBUG] La habitacion en ({0}, {1}) ya se ha visitado".format(x, y))

            return False

        self.mazmorra[y][x] = i_casilla.habitacion if not inicial else i_casilla.inicial
        self.habitaciones[(x_mapa, y_mapa)] = habitacion

        if self.debug:
            print("[DEBUG] Se visita la habitacion ({0}, {1})".format(x, y))

        return True

    def convertir_mazmorra_mapa(self, coordenada):
        return coordenada // self.factor

    def convertir_mapa_mazmorra(self, coordenada):
        factor_medios = self.factor >> 1
        return coordenada * self.factor + factor_medios

    def se_saldria_de_la_mazmorra(self, x, y, direccion):
        x += direccion[0]
        y += direccion[1]

        return x < 0 or y < 0 or x >= self.ancho or y >= self.alto

    def imprimir_mazmorra(self, esconder_vacias=True):
        for fila in self.mazmorra:
            for casilla in fila:
                print(" " if casilla ==
                      i_casilla.vacio and esconder_vacias else casilla, " ", end="")
            print("")

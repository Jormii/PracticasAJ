import importlib
import pygame
import sys
import os
import pathlib
from decimal import Decimal
import math

ANCHO_MONITOR = 1360
ALTO_MONITOR = 768
ESCALA_SPRITES = 128

i_template = importlib.import_module("TemplateMazmorra")
i_mazmorra = importlib.import_module("Mazmorra")
i_casilla = importlib.import_module("Casilla")
i_tesoro = importlib.import_module("Tesoro")
i_vegas = importlib.import_module("LasVegas")
i_matriz_utils = importlib.import_module("MatrizUtils")


def main():
    path = pathlib.Path(__file__).parent.absolute().__str__()
    os.chdir(path)

    pygame.init()
    pygame.display.set_caption("AJ - Practica 2")
    sprites = inicializar_sprites()

    mazmorra = generar_mazmorra()
    pintar_mazmorra(mazmorra, sprites)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    mazmorra.generar_mazmorra()
                    pintar_mazmorra(mazmorra, sprites)
                    pygame.display.flip()


def inicializar_sprites():
    sprites = {}
    sprites["vacia"] = pygame.image.load("./tiles/14.png")
    sprites["uno"] = pygame.image.load("./tiles/6.png")
    sprites["dos_1"] = pygame.image.load("./tiles/1.png")
    sprites["dos_4"] = pygame.image.load("./tiles/4.png")
    sprites["dos_5"] = pygame.image.load("./tiles/5.png")
    sprites["tres_2"] = pygame.image.load("./tiles/2.png")
    sprites["tres_8"] = pygame.image.load("./tiles/8.png")
    sprites["tres_11"] = pygame.image.load("./tiles/11.png")
    # sprites["cuatro"] = pygame.image.load("./tiles/cuatro_conexiones.png")

    return sprites


def generar_mazmorra():
    debug = False

    ancho = i_vegas.random_las_vegas(5, 6 + 1)
    alto = i_vegas.random_las_vegas(5, 6 + 1) + 1
    n_tuneles = i_vegas.random_las_vegas(
        max(ancho, alto), max(ancho, alto) + abs(ancho - alto))
    l_max_tunnel = int(max(ancho, alto) * 2/3)
    template = i_template.TemplateMazmorra(
        ancho, alto, n_tuneles, l_max_tunnel, debug)

    lote_tesoros_1 = i_tesoro.Tesoros(
        [(1, i_tesoro.Tesoro("Tesoro_A")),
         (1, i_tesoro.Tesoro("Tesoro_B"))
         ]
    )
    lote_tesoros_2 = i_tesoro.Tesoros(
        [(1, i_tesoro.Tesoro("Tesoro_1")),
         (1, i_tesoro.Tesoro("Tesoro_2")),
         (2, i_tesoro.Tesoro("Tesoro_3"))
         ]
    )
    lista_tesoros = [lote_tesoros_1, lote_tesoros_2]

    factor = 3
    densidad_maxima = 0.3
    generador = i_mazmorra.Mazmorra(
        template, factor, densidad_maxima, lista_tesoros, debug)
    generador.generar_mazmorra()

    if debug:
        mazmorra.template.imprimir_mapa_detalle()
        mazmorra.imprimir_mazmorra()

    return generador


def pintar_mazmorra(mazmorra, sprites):
    template_mazmorra = mazmorra.template

    ancho = template_mazmorra.ancho * mazmorra.factor
    alto = template_mazmorra.alto * mazmorra.factor

    escala = ESCALA_SPRITES
    ancho_pantalla = ancho * escala
    alto_pantalla = alto * escala

    while ancho_pantalla > ANCHO_MONITOR or alto_pantalla > ALTO_MONITOR:
        ancho_pantalla = ancho_pantalla >> 1
        alto_pantalla = alto_pantalla >> 1
        escala = escala >> 1

    screen = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
    screen.fill((0, 0, 0))

    for fila in mazmorra.mazmorra:
        for casilla in fila:
            # TODO: Quitar
            x = casilla.posicion[0]
            y = casilla.posicion[1]

            n_conexiones = len(casilla.conexiones)
            if n_conexiones == 0:
                pintar_casilla_vacia(casilla, escala, sprites, screen)
            if n_conexiones == 1:
                pintar_casilla_una_conexion(casilla, escala, sprites, screen)
            if n_conexiones == 2:
                pintar_casilla_dos_conexiones(
                    casilla, mazmorra, escala, sprites, screen)
            if n_conexiones == 3:
                pintar_casilla_tres_conexiones(
                    casilla, mazmorra, escala, sprites, screen)
            if n_conexiones == 4:
                color = color_basico(casilla)
                rectangulo = (x * escala, y * escala,
                              escala, escala)
                pygame.draw.rect(screen, color, rectangulo, 0)
                # pintar_casilla_cuatro_conexiones(x, y, escala, sprites, screen)


def pintar_casilla_vacia(casilla, escala, sprites, screen):
    sprite = sprites["vacia"]
    x = casilla.posicion[0]
    y = casilla.posicion[1]
    orientacion = i_vegas.random_las_vegas(0, 4)
    dibujar_sprite(sprite, x, y, orientacion, escala, screen)


def pintar_casilla_una_conexion(casilla, escala, sprites, screen):
    sprite = sprites["uno"]
    x = casilla.posicion[0]
    y = casilla.posicion[1]
    orientacion = casilla.orientacion()
    dibujar_sprite(sprite, x, y, orientacion, escala, screen)


def pintar_casilla_dos_conexiones(casilla, mazmorra, escala, sprites, screen):
    x = casilla.posicion[0]
    y = casilla.posicion[1]

    orientacion = casilla.orientacion()
    # Si orientacion no tiene decimales => No esquina
    if Decimal(orientacion) % 1 == 0:
        sprite = sprites["dos_5"]
    else:
        orientacion = int(orientacion)

        # TODO: Feo
        if orientacion == 1 and i_casilla.direcciones[0] in casilla.conexiones:
            orientacion = 3

        direccion = i_casilla.direcciones[orientacion]
        x_conexion = x + direccion[0]
        y_conexion = y + direccion[1]

        casilla_adyacente = mazmorra.mazmorra[y_conexion][x_conexion]
        conexion_perpendicular = i_casilla.direcciones[(orientacion + 1) % 4]
        sprite = sprites["dos_1"] if conexion_perpendicular in casilla_adyacente.conexiones else sprites["dos_4"]

    dibujar_sprite(sprite, x, y, orientacion, escala, screen)


def pintar_casilla_tres_conexiones(casilla, mazmorra, escala, sprites, screen):
    x = casilla.posicion[0]
    y = casilla.posicion[1]

    orientacion = int(casilla.orientacion())

    # TODO: Muy feo
    if orientacion == 1:
        if i_casilla.direcciones[2] not in casilla.conexiones:
            orientacion = 0
        elif i_casilla.direcciones[1] not in casilla.conexiones:
            orientacion = 3

    direccion_orientacion = i_casilla.direcciones[orientacion]
    x_adyacente = x + direccion_orientacion[0]
    y_adyacente = y + direccion_orientacion[1]
    casilla_adyacente = mazmorra.mazmorra[y_adyacente][x_adyacente]

    direccion_perpendicular_izq = i_casilla.direcciones[(orientacion - 1) % 4]
    direccion_perpendicular_der = i_casilla.direcciones[(orientacion + 1) % 4]

    adyacente_conecta_izq = direccion_perpendicular_izq in casilla_adyacente.conexiones
    adyacente_conecta_der = direccion_perpendicular_der in casilla_adyacente.conexiones

    if not adyacente_conecta_izq and not adyacente_conecta_der:
        sprite = sprites["tres_8"]
    elif adyacente_conecta_izq and adyacente_conecta_der:
        sprite = sprites["tres_2"]
    else:
        sprite = sprites["tres_11"]
        flip_horizontal = bool(abs(direccion_orientacion[1])) and adyacente_conecta_izq
        flip_vertical = bool(abs(direccion_orientacion[0])) and adyacente_conecta_izq
        sprite = pygame.transform.flip(sprite, flip_horizontal, flip_vertical).convert()

    dibujar_sprite(sprite, x, y, orientacion, escala, screen)


def pintar_casilla_cuatro_conexiones(casilla, mazmorra, escala, sprites, screen):
    x = 0


def dibujar_sprite(sprite, x, y, orientacion, escala, screen):
    rotacion = -90 * orientacion
    sprite = pygame.transform.scale(sprite, (escala, escala)).convert()
    sprite = pygame.transform.rotate(sprite, rotacion).convert()

    screen.blit(sprite, (x * escala, y * escala))


def color_basico(casilla):
    if casilla.esta_vacia():
        color = (0, 0, 0)
    elif casilla.es_tunel():
        color = (255 >> 1, 255 >> 1, 255 >> 1)
    elif casilla.almacena_tesoro():
        color = (0, 255, 0)
    elif casilla.es_casilla_inicial:
        color = (255, 0, 0)
    elif casilla.es_habitacion():
        color = (255, 255, 255)

    return color


if __name__ == "__main__":
    main()

import importlib
import pygame
import sys
import os
import pathlib
from decimal import Decimal
import math

ANCHO_MONITOR = 1360
ALTO_MONITOR = 768
ESCALA_SPRITES = 24

PREFIJOS_SPRITES = {
    "tunel": "water_",
    "inicial": "initial_"
}

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
    for k, prefijo in PREFIJOS_SPRITES.items():
        sprites_prefijo = {}
        sprites[k] = sprites_prefijo

        sprites_prefijo["vacia"] = pygame.image.load(
            "./tiles/{0}empty.png".format(prefijo))

        sprites_prefijo["uno"] = pygame.image.load(
            "./tiles/{0}6.png".format(prefijo))

        sprites_prefijo["dos_1"] = pygame.image.load(
            "./tiles/{0}1.png".format(prefijo))
        sprites_prefijo["dos_4"] = pygame.image.load(
            "./tiles/{0}4.png".format(prefijo))
        sprites_prefijo["dos_5"] = pygame.image.load(
            "./tiles/{0}5.png".format(prefijo))

        sprites_prefijo["tres_2"] = pygame.image.load(
            "./tiles/{0}2.png".format(prefijo))
        sprites_prefijo["tres_8"] = pygame.image.load(
            "./tiles/{0}8.png".format(prefijo))
        sprites_prefijo["tres_11"] = pygame.image.load(
            "./tiles/{0}11.png".format(prefijo))
        sprites_prefijo["tres_11"] = pygame.image.load(
            "./tiles/{0}11.png".format(prefijo))

        sprites_prefijo["cuatro_3"] = pygame.image.load(
            "./tiles/{0}3.png".format(prefijo))
        sprites_prefijo["cuatro_7"] = pygame.image.load(
            "./tiles/{0}7.png".format(prefijo))
        sprites_prefijo["cuatro_9"] = pygame.image.load(
            "./tiles/{0}9.png".format(prefijo))
        sprites_prefijo["cuatro_10"] = pygame.image.load(
            "./tiles/{0}10.png".format(prefijo))
        sprites_prefijo["cuatro_12"] = pygame.image.load(
            "./tiles/{0}12.png".format(prefijo))
        sprites_prefijo["cuatro_13"] = pygame.image.load(
            "./tiles/{0}13.png".format(prefijo))

    return sprites


def generar_mazmorra():
    debug = False

    ancho = 15
    alto = 8
    n_tuneles = i_vegas.random_las_vegas(
        max(ancho, alto), max(ancho, alto) + abs(ancho - alto) + 1)
    l_max_tunnel = max(ancho, alto)
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
    densidad_maxima = 0.25
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

    indice_aleatorio = i_vegas.random_las_vegas(0, len(PREFIJOS_SPRITES))
    tileset = list(PREFIJOS_SPRITES.keys())[indice_aleatorio]
    subconjunto_sprites = sprites[tileset]
    for fila in mazmorra.mazmorra:
        for casilla in fila:
            n_conexiones = len(casilla.conexiones)
            if n_conexiones == 0:
                pintar_casilla_vacia(
                    casilla, escala, subconjunto_sprites, screen)
            if n_conexiones == 1:
                pintar_casilla_una_conexion(
                    casilla, escala, subconjunto_sprites, screen)
            if n_conexiones == 2:
                pintar_casilla_dos_conexiones(
                    casilla, mazmorra, escala, subconjunto_sprites, screen)
            if n_conexiones == 3:
                pintar_casilla_tres_conexiones(
                    casilla, mazmorra, escala, subconjunto_sprites, screen)
            if n_conexiones == 4:
                pintar_casilla_cuatro_conexiones(
                    casilla, mazmorra, escala, subconjunto_sprites, screen)


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
    elif not adyacente_conecta_izq and adyacente_conecta_der:
        sprite = sprites["tres_11"]
    else:
        sprite = sprites["tres_11"]
        flip_horizontal = True
        flip_vertical = False
        sprite = pygame.transform.flip(
            sprite, flip_horizontal, flip_vertical).convert()

    dibujar_sprite(sprite, x, y, orientacion, escala, screen)


def pintar_casilla_cuatro_conexiones(casilla, mazmorra, escala, sprites, screen):
    x = casilla.posicion[0]
    y = casilla.posicion[1]

    conexiones_adyacentes = []
    for direccion in casilla.conexiones:
        x_casilla_adyacente = x + direccion[0]
        y_casilla_adyacente = y + direccion[1]
        casilla_adyacente = mazmorra.mazmorra[y_casilla_adyacente][x_casilla_adyacente]

        orientacion_direccion = i_casilla.orientaciones[direccion]
        direccion_perpendicular = i_casilla.direcciones[(
            orientacion_direccion + 1) % 4]

        if direccion_perpendicular in casilla_adyacente.conexiones:
            conexiones_adyacentes.append(direccion)

    orientacion = 0
    n_conexiones_adyacentes = len(conexiones_adyacentes)
    if n_conexiones_adyacentes == 0:
        sprite = sprites["cuatro_7"]
        orientacion = i_vegas.random_las_vegas(0, 4)
    elif n_conexiones_adyacentes == 1:
        sprite = sprites["cuatro_12"]
        orientacion = i_casilla.orientaciones[conexiones_adyacentes[0]]
    elif n_conexiones_adyacentes == 2:
        conexion_1 = conexiones_adyacentes[0]
        conexion_2 = conexiones_adyacentes[1]

        # Si son opuestos
        if conexion_1[0] + conexion_2[0] == 0:
            sprite = sprites["cuatro_13"]
            orientacion = i_casilla.orientaciones[conexion_1]
        else:
            sprite = sprites["cuatro_9"]

            orientacion_1 = i_casilla.orientaciones[conexiones_adyacentes[0]]
            orientacion_2 = i_casilla.orientaciones[conexiones_adyacentes[1]]

            # TODO: Muy feo
            orientacion = max(orientacion_1, orientacion_2)
            if orientacion == 3:
                if orientacion_1 == 0:
                    orientacion = 0

    elif n_conexiones_adyacentes == 3:
        sprite = sprites["cuatro_10"]

        for direccion in i_casilla.direcciones.values():
            if not direccion in conexiones_adyacentes:
                adyacencia_no_existente = direccion
                break

        orientacion = i_casilla.orientaciones[adyacencia_no_existente]
    elif n_conexiones_adyacentes == 4:
        sprite = sprites["cuatro_3"]
        orientacion = i_vegas.random_las_vegas(0, 4)

    dibujar_sprite(sprite, x, y, orientacion, escala, screen)


def dibujar_sprite(sprite, x, y, orientacion, escala, screen):
    rotacion = -90 * orientacion
    sprite = pygame.transform.scale(sprite, (escala, escala)).convert()
    sprite = pygame.transform.rotate(sprite, rotacion).convert()

    screen.blit(sprite, (x * escala, y * escala))


if __name__ == "__main__":
    main()

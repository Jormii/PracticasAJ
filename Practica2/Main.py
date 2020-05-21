import os
import sys
import pathlib
import importlib
import pygame

from os import system
from decimal import Decimal

i_template = importlib.import_module("TemplateMazmorra")
i_mazmorra = importlib.import_module("Mazmorra")
i_casilla = importlib.import_module("Casilla")
i_tesoro = importlib.import_module("Tesoro")
i_vegas = importlib.import_module("LasVegas")

ANCHO_MONITOR = 1360
ALTO_MONITOR = 768

ESCALA_SPRITES = 24
ESCALA_SPRITES_OBJETOS = 16
PINTAR_SPRITES = True
SPRITES_A_USAR = "agua"
PREFIJOS_SPRITES = {
    "agua": "water_",
    "gemas": "initial_"
}


def main():
    # Cambiar el path para hacer el directorio que contiene Main.py el cwd
    path = pathlib.Path(__file__).parent.absolute().__str__()
    os.chdir(path)

    generador_de_mazmorra = inicializar_mazmorra()
    screen, escala = inicializar_screen(generador_de_mazmorra)

    sprites = inicializar_sprites()
    pintar_mazmorra(generador_de_mazmorra, sprites, screen, escala)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    global PINTAR_SPRITES
                    PINTAR_SPRITES = not PINTAR_SPRITES
                    pintar_mazmorra(generador_de_mazmorra,
                                    sprites, screen, escala)
                if event.key == pygame.K_e:
                    system("clear")
                    generador_de_mazmorra.template.random_walk()
                    generador_de_mazmorra.generar_mazmorra()
                    pintar_mazmorra(generador_de_mazmorra,
                                    sprites, screen, escala)
                if event.key == pygame.K_w:
                    system("clear")
                    generador_de_mazmorra.generar_mazmorra()
                    pintar_mazmorra(generador_de_mazmorra,
                                    sprites, screen, escala)


def inicializar_mazmorra():
    debug = False

    template = inicializar_template_mazmorra(debug)
    lista_objetos = inicializar_objetos()
    generador = inicializar_generador(template, lista_objetos, debug)
    generador.generar_mazmorra()

    return generador


def inicializar_template_mazmorra(debug):
    ancho = 13
    alto = 7
    n_tuneles = i_vegas.random_las_vegas(
        max(ancho, alto), max(ancho, alto) + abs(ancho - alto) + 1)
    l_max_tunel = int(max(ancho, alto) * 2 * 1/3)

    return i_template.TemplateMazmorra(
        ancho, alto, n_tuneles, l_max_tunel, debug)


def inicializar_objetos():
    # Lista con tuplas probabilidad-objeto
    # La clase Tesoros se encarga de normalizar estas probabilidades
    objetos = i_tesoro.Tesoros(
        [(70, i_tesoro.Tesoro("Baya", "baya")),
         (20, i_tesoro.Tesoro("Llave", "llave")),
         (8, i_tesoro.Tesoro("Manzana", "manzana")),
         (2, i_tesoro.Tesoro("Semilla", "semilla"))
         ]
    )

    tesoros = i_tesoro.Tesoros(
        [(82, i_tesoro.Tesoro("Dinero", "dinero")),
         (10, i_tesoro.Tesoro("Pocion", "pocion")),
         (8, i_tesoro.Tesoro("Tesoro", "tesoro"))
         ]
    )

    return [objetos, tesoros]


def inicializar_generador(template, lista_objetos, debug):
    factor = 3
    densidad_maxima = 0.4
    return i_mazmorra.Mazmorra(
        template, factor, densidad_maxima, lista_objetos, debug)


def inicializar_screen(mazmorra):
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

    pygame.init()
    pygame.display.set_caption("AJ - Practica 2 - Jorge López Natal")
    screen = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
    screen.fill((0, 0, 0))

    return screen, escala


def inicializar_sprites():
    prefijo = PREFIJOS_SPRITES[SPRITES_A_USAR]

    sprites = {}

    sprites["vacia"] = pygame.image.load(
        "./tiles/{0}empty.png".format(prefijo))

    sprites["uno"] = pygame.image.load(
        "./tiles/{0}6.png".format(prefijo))

    sprites["dos_1"] = pygame.image.load(
        "./tiles/{0}1.png".format(prefijo))
    sprites["dos_4"] = pygame.image.load(
        "./tiles/{0}4.png".format(prefijo))
    sprites["dos_5"] = pygame.image.load(
        "./tiles/{0}5.png".format(prefijo))

    sprites["tres_2"] = pygame.image.load(
        "./tiles/{0}2.png".format(prefijo))
    sprites["tres_8"] = pygame.image.load(
        "./tiles/{0}8.png".format(prefijo))
    sprites["tres_11"] = pygame.image.load(
        "./tiles/{0}11.png".format(prefijo))
    sprites["tres_11"] = pygame.image.load(
        "./tiles/{0}11.png".format(prefijo))

    sprites["cuatro_3"] = pygame.image.load(
        "./tiles/{0}3.png".format(prefijo))
    sprites["cuatro_7"] = pygame.image.load(
        "./tiles/{0}7.png".format(prefijo))
    sprites["cuatro_9"] = pygame.image.load(
        "./tiles/{0}9.png".format(prefijo))
    sprites["cuatro_10"] = pygame.image.load(
        "./tiles/{0}10.png".format(prefijo))
    sprites["cuatro_12"] = pygame.image.load(
        "./tiles/{0}12.png".format(prefijo))
    sprites["cuatro_13"] = pygame.image.load(
        "./tiles/{0}13.png".format(prefijo))

    sprites["baya"] = pygame.image.load("./items/baya.png")
    sprites["dinero"] = pygame.image.load("./items/dinero.png")
    sprites["llave"] = pygame.image.load("./items/llave.png")
    sprites["manzana"] = pygame.image.load("./items/manzana.png")
    sprites["pocion"] = pygame.image.load("./items/pocion.png")
    sprites["semilla"] = pygame.image.load("./items/semilla.png")
    sprites["tesoro"] = pygame.image.load("./items/tesoro.png")

    return sprites


def pintar_mazmorra(generador_de_mazmorra, sprites, screen, escala):
    mazmorra = generador_de_mazmorra.mazmorra
    for fila in mazmorra:
        for casilla in fila:
            pintar_casilla(casilla, mazmorra, escala, sprites, screen)

            if casilla.almacena_tesoro():
                pintar_tesoro(casilla, escala, sprites, screen)

    pygame.display.flip()


def pintar_casilla(casilla, mazmorra, escala, sprites, screen):
    if not PINTAR_SPRITES:
        if casilla.esta_vacia():
            color = (0, 0, 0)
        elif casilla.es_tunel():
            color = (122, 122, 122)
        elif casilla.es_casilla_inicial:
            color = (255, 0, 0)
        elif casilla.es_habitacion():
            color = (255, 255, 255)

        x = casilla.posicion[0]
        y = casilla.posicion[1]
        pygame.draw.rect(screen, color, (escala * x,
                                         escala * y, escala, escala))
        return

    # Nota: Las siguientes funciones son bastante feas y caoticas
    n_conexiones = len(casilla.conexiones)
    if n_conexiones == 0:
        pintar_casilla_vacia(
            casilla, escala, sprites, screen)
    if n_conexiones == 1:
        pintar_casilla_una_conexion(
            casilla, escala, sprites, screen)
    if n_conexiones == 2:
        pintar_casilla_dos_conexiones(
            casilla, mazmorra, escala, sprites, screen)
    if n_conexiones == 3:
        pintar_casilla_tres_conexiones(
            casilla, mazmorra, escala, sprites, screen)
    if n_conexiones == 4:
        pintar_casilla_cuatro_conexiones(
            casilla, mazmorra, escala, sprites, screen)


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

        casilla_adyacente = mazmorra[y_conexion][x_conexion]
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
    casilla_adyacente = mazmorra[y_adyacente][x_adyacente]

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
        casilla_adyacente = mazmorra[y_casilla_adyacente][x_casilla_adyacente]

        orientacion_direccion = i_casilla.orientaciones[direccion]
        direccion_perpendicular = i_casilla.direcciones[(
            orientacion_direccion + 1) % 4]

        if direccion_perpendicular in casilla_adyacente.conexiones:
            conexiones_adyacentes.append(direccion)

    orientacion = 0
    n_conexiones_adyacentes = len(conexiones_adyacentes)
    if n_conexiones_adyacentes == 0:
        sprite = sprites["cuatro_7"]
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

    dibujar_sprite(sprite, x, y, orientacion, escala, screen)


def pintar_tesoro(casilla, escala, sprites, screen):
    if not PINTAR_SPRITES:
        x = casilla.posicion[0]
        y = casilla.posicion[1]
        color = (0, 255, 00)
        pygame.draw.rect(screen, color, (escala * x,
                                         escala * y, escala, escala))
        return

    tesoro = casilla.tesoro

    sprite = sprites[tesoro.clave_sprite]
    x = casilla.posicion[0]
    y = casilla.posicion[1]
    orientacion = 0

    escala_tesoro = int(
        escala * ESCALA_SPRITES_OBJETOS / ESCALA_SPRITES)
    sprite = pygame.transform.scale(
        sprite, (escala_tesoro, escala_tesoro))
    dibujar_sprite(sprite, x, y, orientacion,
                   escala, screen, escalar=False)


def dibujar_sprite(sprite, x, y, orientacion, escala, screen, escalar=True):
    rotacion = -90 * orientacion

    if escalar:
        sprite = pygame.transform.scale(sprite, (escala, escala))
    sprite = pygame.transform.rotate(sprite, rotacion)

    screen.blit(sprite, (x * escala, y * escala))


if __name__ == "__main__":
    main()

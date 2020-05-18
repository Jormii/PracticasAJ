import importlib
import pygame
import sys

ANCHO_MONITOR = 1360
ALTO_MONITOR = 768
ESCALA_SPRITES = 24

i_template = importlib.import_module("TemplateMazmorra")
i_mazmorra = importlib.import_module("Mazmorra")
i_casilla = importlib.import_module("Casilla")
i_tesoro = importlib.import_module("Tesoro")


def main():
    pygame.init()
    pygame.display.set_caption("AJ - Practica 2")
    # sprites = inicializar_sprites()
    sprites = {}

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
    sprites["vacio"] = pygame.image.load("./sprites/sin_conexiones.png")
    sprites["uno"] = pygame.image.load("./sprites/una_conexion.png")
    sprites["dos"] = pygame.image.load("./sprites/dos_conexiones.png")
    sprites["tres"] = pygame.image.load("./sprites/tres_conexiones.png")
    sprites["cuatro"] = pygame.image.load("./sprites/cuatro_conexiones.png")

    return sprites


def generar_mazmorra():
    debug = True

    ancho = 3
    alto = 3
    n_tuneles = 3
    l_max_tunnel = 3
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
    densidad_maxima = 0.4
    generador = i_mazmorra.Mazmorra(
        template, factor, densidad_maxima, lista_tesoros)
    generador.generar_mazmorra()

    return generador


def pintar_mazmorra(mazmorra, sprites):
    mazmorra.template.imprimir_mapa_detalle()
    # mazmorra.imprimir_mazmorra()

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

    for x in range(ancho):
        for y in range(alto):
            celda = mazmorra.mazmorra[y][x]
            if celda.esta_vacia():
                color = (0, 0, 0)
                # pintar_casilla_vacia(x, y, escala, sprites, screen)
            elif celda.es_tunel():
                color = (255 >> 1, 255 >> 1, 255 >> 1)
            elif celda.es_habitacion() and not celda.es_casilla_inicial:
                color = (255, 255, 255)
            elif celda.es_casilla_inicial:
                color = (255, 0, 0)
            elif celda == i_casilla.tesoro:
                color = (0, 255, 0)

            rectangulo = (x * escala, y * escala,
                          escala, escala)
            pygame.draw.rect(screen, color, rectangulo, 0)


def pintar_casilla_vacia(x, y, escala, sprites, screen):
    sprite = pygame.transform.scale(
        sprites["vacio"], (escala, escala)).convert()
    screen.blit(sprite, (x * escala, y * escala))


if __name__ == "__main__":
    main()

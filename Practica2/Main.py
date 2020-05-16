import importlib
import pygame
import sys

ANCHO_MONITOR = 1360
ALTO_MONITOR = 768
ESCALA_SPRITES = 96

i_template = importlib.import_module("TemplateMazmorra")
i_mazmorra = importlib.import_module("Mazmorra")
i_casilla = importlib.import_module("Casilla")


def main():
    pygame.init()
    pygame.display.set_caption("AJ - Practica 2")

    mazmorra = generar_mazmorra()
    pintar_mazmorra(mazmorra)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    mazmorra.generar_mazmorra()
                    pintar_mazmorra(mazmorra)
                    pygame.display.flip()


def generar_mazmorra():
    ancho = 15
    alto = 15
    n_tuneles = 15
    l_max_tunnel = 15
    template = i_template.TemplateMazmorra(
        ancho, alto, n_tuneles, l_max_tunnel)

    factor = 3
    densidad_maxima = 0.4
    generador = i_mazmorra.Mazmorra(template, factor, densidad_maxima, False)
    generador.generar_mazmorra()

    return generador


def pintar_mazmorra(mazmorra):
    # mazmorra.template.imprimir_mapa_detalle()
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
            if celda == i_casilla.vacio:
                color = (0, 0, 0)
            elif celda == i_casilla.tunel:
                color = (255 >> 1, 255 >> 1, 255 >> 1)
            elif celda == i_casilla.habitacion:
                color = (255, 255, 255)
            elif celda == i_casilla.inicial:
                color = (255, 0, 0)

            rectangulo = (x * escala, y * escala,
                          escala, escala)
            pygame.draw.rect(screen, color, rectangulo, 0)


if __name__ == "__main__":
    main()

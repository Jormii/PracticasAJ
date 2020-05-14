import importlib
import pygame
import sys

ESCALA_SPRITES = 128

t = importlib.import_module("TemplateMazmorra")
m = importlib.import_module("Mazmorra")
c = importlib.import_module("Casilla")


def main():
    pygame.init()
    pygame.display.set_caption("AJ - Practica 2")

    template_mazmorra = generar_mazmorra()
    pintar_mazmorra(template_mazmorra)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


def generar_mazmorra():
    ancho = 3
    alto = 3
    n_tuneles = 2
    l_max_tunnel = 5
    template = t.TemplateMazmorra(ancho, alto, n_tuneles, l_max_tunnel)

    template.random_walk()
    return template

    # factor = 3
    # densidad_maxima = 0.8
    # generador = m.Mazmorra(template, factor, densidad_maxima)
    # mazmorra = generador.generar_mazmorra()

    # template.imprimir_mapa()
    # print("---")
    # generador.imprimir_mazmorra()


def pintar_mazmorra(template_mazmorra):
    template_mazmorra.imprimir_mapa_detalle()

    ancho_pantalla = template_mazmorra.ancho * ESCALA_SPRITES
    alto_pantalla = template_mazmorra.alto * ESCALA_SPRITES
    screen = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
    screen.fill((0, 0, 0))

    for x in range(template_mazmorra.ancho):
        for y in range(template_mazmorra.alto):
            casilla = template_mazmorra.mapa[y][x]
            if casilla.tipo == c.vacio:
                color = (0, 0, 0)
            elif casilla.tipo == c.tunel:
                color = (255 >> 1, 255 >> 1, 255 >> 1)
            elif casilla.tipo == c.habitacion:
                color = (255, 255, 255)

            rectangulo = (x * ESCALA_SPRITES, y * ESCALA_SPRITES,
                          ESCALA_SPRITES, ESCALA_SPRITES)
            pygame.draw.rect(screen, color, rectangulo, 0)

    x0 = template_mazmorra.posicion_inicial[0]
    y0 = template_mazmorra.posicion_inicial[1]
    rectangulo = (x0 * ESCALA_SPRITES, y0 * ESCALA_SPRITES,
                  ESCALA_SPRITES, ESCALA_SPRITES)
    pygame.draw.rect(screen, (255, 0, 0), rectangulo, 0)


if __name__ == "__main__":
    main()

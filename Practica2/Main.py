import importlib

if __name__ == "__main__":
    t = importlib.import_module("TemplateMazmorra")
    m = importlib.import_module("Mazmorra")

    ancho = 4
    alto = 4
    n_tuneles = 7
    l_max_tunnel = 5
    template = t.TemplateMazmorra(ancho, alto, n_tuneles, l_max_tunnel)

    factor = 3
    generador = m.Mazmorra(template, factor)

    mapa, casilla_inicial = template.random_walk()
    template.imprimir_mapa_detalle()
    print()
    template.imprimir_mapa()

    mazmorra = generador.generar_mazmorra()
    print()
    generador.imprimir_mazmorra()
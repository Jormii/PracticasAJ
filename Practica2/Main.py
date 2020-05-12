import importlib

if __name__ == "__main__":
    t = importlib.import_module("TemplateMazmorra")
    m = importlib.import_module("Mazmorra")
    c = importlib.import_module("Casilla")

    ancho = 3
    alto = 3
    n_tuneles = 10
    l_max_tunnel = 5
    template = t.TemplateMazmorra(ancho, alto, n_tuneles, l_max_tunnel)

    factor = 3
    densidad_maxima = 0.8
    generador = m.Mazmorra(template, factor, densidad_maxima)
    mazmorra = generador.generar_mazmorra()
    
    template.imprimir_mapa()
    print("---")
    generador.imprimir_mazmorra()

    x = 0
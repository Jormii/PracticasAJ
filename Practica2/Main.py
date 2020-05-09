import importlib

if __name__ == "__main__":
    t = importlib.import_module("TemplateMazmorra")
    m = importlib.import_module("Mazmorra")
    
    ancho = 2
    alto = 2
    n_tuneles = 1
    l_max_tunnel = 1
    template = t.TemplateMazmorra(ancho, alto, n_tuneles, l_max_tunnel)
    
    factor = 3
    generador = m.Mazmorra(template, factor)
    
    mapa, casilla_inicial = template.random_walk()
    template.imprimir_mapa()
    
    mazmorra = generador.generar_mazmorra()
    generador.imprimir_mazmorra()
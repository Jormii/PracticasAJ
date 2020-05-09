import importlib

if __name__ == "__main__":
    t = importlib.import_module("TemplateMazmorra")
    m = importlib.import_module("Mazmorra")
    
    ancho = 3
    alto = 3
    n_tuneles = 1
    l_max_tunnel = 3
    template = t.TemplateMazmorra(ancho, alto, n_tuneles, l_max_tunnel, True)
    mapa, casilla_inicial = template.random_walk()
    template.imprimir_mapa()
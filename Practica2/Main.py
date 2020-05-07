import importlib

if __name__ == "__main__":
    t = importlib.import_module("TemplateMazmorra")
    m = importlib.import_module("Mazmorra")
    
    ancho = 4
    alto = 4
    n_tuneles = 3
    l_max_tunnel = 5
    template = t.TemplateMazmorra(ancho, alto, n_tuneles, l_max_tunnel, True)
    template.random_walk()
    template.imprimir_mapa()
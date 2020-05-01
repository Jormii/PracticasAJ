import importlib

if __name__ == "__main__":
    rw = importlib.import_module("RandomWalk")
    
    ancho = 5
    alto = 5
    n_tuneles = 2
    l_max_tunnel = 5
    mapa = rw.random_walk(ancho, alto, n_tuneles, l_max_tunnel, True)
    rw.imprimir_mapa(mapa)
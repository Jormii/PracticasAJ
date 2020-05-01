import importlib

if __name__ == "__main__":
    rw = importlib.import_module("RandomWalk")
    
    ancho = 5
    alto = 5
    n_tuneles = 3
    l_max_tunnel = 6
    mapa = rw.random_walk(ancho, alto, n_tuneles, l_max_tunnel)
    rw.imprimir_mapa(mapa)
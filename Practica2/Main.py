import importlib

if __name__ == "__main__":
    rw = importlib.import_module("RandomWalk")
    
    ancho = 4
    alto = 4
    n_tuneles = 3
    l_max_tunnel = 5
    mapa = rw.random_walk(ancho, alto, n_tuneles, l_max_tunnel)
    rw.imprimir_mapa(mapa)
import importlib

i_casilla = importlib.import_module("Casilla")
i_vegas = importlib.import_module("LasVegas")


def pertenece_a_matriz(posicion, ancho, alto):
    x = posicion[0]
    y = posicion[1]
    return x >= 0 and y >= 0 and x < ancho and y < alto


def se_saldria_de_la_matriz(posicion, direccion, ancho, alto):
    x = posicion[0] + direccion[0]
    y = posicion[1] + direccion[1]
    return not pertenece_a_matriz((x, y), ancho, alto)


# Utilizada en los giros de los tuneles
def calcular_nueva_direccion(posicion, direccion, ancho, alto):
    x = posicion[0]
    y = posicion[1]
    direcciones = i_casilla.direcciones

    # Se mueve hacia el norte o sur
    if direccion[0] == 0:
        # %x € {0, 1}, si extremo izquierdo/derecho
        porcentaje_en_x = x / (ancho - 1) * 100
        girar_derecha = i_vegas.random_las_vegas(1, 100 + 1) > porcentaje_en_x
        nueva_direccion = direcciones[1] if girar_derecha else direcciones[3]
    # Se mueve hacia el oeste o este
    else:
        # %y € {0, 1}, si extremo superior/inferior
        porcentaje_en_y = y / (alto - 1) * 100
        girar_abajo = i_vegas.random_las_vegas(1, 100 + 1) > porcentaje_en_y
        nueva_direccion = direcciones[2] if girar_abajo else direcciones[0]

    return nueva_direccion

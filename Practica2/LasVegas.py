import importlib

i_lcm = importlib.import_module("LCM")


def random_las_vegas(lim_inf, lim_sup):
    diferencia = lim_sup - lim_inf
    random = i_lcm.lcm_random() // (i_lcm.c["M"] // diferencia)
    while random >= diferencia:
        random = i_lcm.lcm_random() // (i_lcm.c["M"] // diferencia)

    return random + lim_inf

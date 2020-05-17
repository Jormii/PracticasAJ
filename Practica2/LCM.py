import datetime
import time

date = datetime.datetime.now()
seed = int(time.mktime(date.timetuple()))
c = {
    "M": 2 ** 10 - 3,
    "A": 35,
    "C": 8,
    "X": seed
}


def lcm_random():
    random = (c["A"] * c["X"]) % c["M"]
    random = modulo_sum(random, c["C"], c["M"])
    c["X"] = random
    return random


def modulo_sum(x, y, m):
    if x <= m - 1 - y:
        return x + y
    else:
        return x - (m - y)
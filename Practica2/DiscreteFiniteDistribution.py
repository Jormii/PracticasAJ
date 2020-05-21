import importlib

i_vegas = importlib.import_module("LasVegas")


def find_smallest_index(S, k):
    for i in range(1, len(S)):
        if S[i - 1] < k <= S[i]:
            return i

    return len(S) - 1


def random_from_weights(W):
    n = len(W)
    S = [0] * n
    S[0] = W[0]
    for i in range(1, n):
        S[i] = S[i - 1] + W[i]

    k = i_vegas.random_las_vegas(1, S[n - 1] - 1)
    if k <= S[0]:
        random = 0
    else:
        random = find_smallest_index(S, k)

    return random

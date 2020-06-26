# Levensthein Distance

from itertools import product
from .utils import init_matrix


def levenshtein(a, b, costs = (1, 1, 1)):
    """Returns the Levensthein distance between two strings"""
    # unpack cost parameters
    del_cost, ins_cost, sub_cost = costs
    # init matrix
    rows, cols, dist = init_matrix(a, b)
    # fill matrix
    for x, y in product(range(1, rows), range(1, cols)):
        if a[x-1] == b[y-1]:
            cost = 0
        else:
            cost = sub_cost
        substitute = dist[x-1][y-1] + cost
        insert = dist[x-1][y] + ins_cost
        delete = dist[x][y-1] + del_cost
        dist[x][y] = min(substitute, insert, delete)
    return dist[x][y]
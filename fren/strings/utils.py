from math import log


def log_odd_ratio(a, b):
    return 2 * log(a/b, 2)


def init_matrix(a, b, factor = 1):
    """Returns rows, cols and sequence matrix needed to init sequence algorithm

    First row and column are indexed and multiplied by `factor`
    [[0, 1, 2, 3],
     [1, 0, 0, 0],
     [2, 0, 0, 0]]
    """
    # dimensions
    rows = len(a)+1
    cols = len(b)+1
    # init with zeros
    matrix = [[0 for i in range(cols)] for j in range(rows)]
    # fill first col
    for row in range(1, rows):
        matrix[row][0] = row * factor
    # fill first row
    for col in range(1, cols):
        matrix[0][col] = col * factor
    return rows, cols, matrix
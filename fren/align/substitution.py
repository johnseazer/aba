def add_to_submat(a, b, n, submat):
    if a not in submat:
        submat[a] = {b: n}
    else:
        submat[a].update({b: n})
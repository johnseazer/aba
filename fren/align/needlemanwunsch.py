# Needleman-Wunsch Algorithm

from itertools import product
from .utils import init_matrix


def align(a, b, scores = (1, -1, -1), submat = {}): 
    """Returns alignment of sequences a and b.

    :param scores: Scores for match award, mismatch penalty and gap penalty
    :type scores: tuple (match, mismatch, gap)
    """
    align_matrix = matrix(a, b, scores, submat)
    align_a, align_b = traceback(a, b, align_matrix, scores, submat)
    return align_a, align_b

def matrix(a, b, scores, submat):
    # unpack score parameters
    _, _, gap_penalty = scores
    # init matrix
    rows, cols, matrix = init_matrix(a, b, factor = gap_penalty)
    # compute cells
    for x, y in product(range(1, rows), range(1, cols)):
        # compute values from top, left, and top-left diagonal cells
        match = matrix[x-1][y-1] + score(a[x-1], b[y-1], scores, submat)
        insert = matrix[x][y-1] + gap_penalty
        delete = matrix[x-1][y] + gap_penalty
        # store maxs
        matrix[x][y] = max(match, delete, insert)
    return matrix

def traceback(a, b, matrix, scores, submat):
    # unpack score parameters
    _, _, gap_penalty = scores
    # init traceback
    align_a = []
    align_b = []
    x = len(a)
    y = len(b)
    # traceback
    while x > 0 or y > 0:
        # retrieve scores
        current_score = matrix[x][y]
        topleft_score = matrix[x-1][y-1]
        left_score = matrix[x][y-1]
        top_score = matrix[x-1][y]
        # find origin cell, append corresponding elements, advance
        if (x > 0 and y > 0
            and current_score == topleft_score + score(a[x-1], b[y-1], scores, submat)):
            # origin is top-left
            align_a.append(a[x-1])
            align_b.append(b[y-1])
            x = x-1
            y = y-1
        elif x > 0 and current_score == top_score + gap_penalty:
            # origin is top
            align_a.append(a[x-1])
            align_b.append('¤')
            x = x-1
        elif y > 0 and current_score == left_score + gap_penalty:
            # origin is left
            align_a.append('¤')
            align_b.append(b[y-1])
            y = y-1
        else:
            raise ValueError('Traceback failed')
    # reverse sequence order
    align_a = align_a[::-1]
    align_b = align_b[::-1]
    return(align_a, align_b)

def score(a, b, scores, submat):
    # unpack score parameters
    match_award, mismatch_penalty, gap_penalty = scores
    # make all lowercase
    a = a.lower()
    b = b.lower()
    # substitution matrix
    if (a in submat and b in submat[a]):
      return submat[a][b]
    # match
    elif (a == b):
        return match_award
    # gap
    elif a == '¤' or b == '¤':
        return gap_penalty
    # mismatch
    else:
        return mismatch_penalty
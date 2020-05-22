#!/usr/bin/env python
# coding: utf-8




# # Needlmann-Wunsch

# ## Implementation

# In[1]:


# scoring values
gap_penalty = -1
match_award = 1
mismatch_penalty = -1

def zeros(rows, cols):
    '''returns a matrix of zeros'''
    res = []
    for x in range(rows):
        res.append([])
        for y in range(cols):
            res[-1].append(0)
    return res

def match_score(a, b):
    if a == b:
        return match_award
    elif a == '-' or b == '-':
        return gap_penalty
    else:
        return mismatch_penalty

def needleman_wunsch(seq1, seq2): 
    
    # init matrix
    n = len(seq1)
    m = len(seq2)
    score = zeros(m + 1, n + 1)
    
    # fill matrix
    
    # first col
    for i in range(0, m + 1):
        score[i][0] = gap_penalty * i
    # first row
    for j in range(0, n + 1):
        score[0][j] = gap_penalty * j
    
    # rest
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # chek top, left, and diagonal cells
            match = score[i - 1][j - 1] + match_score(seq1[j-1], seq2[i-1])
            delete = score[i - 1][j] + gap_penalty
            insert = score[i][j - 1] + gap_penalty
            # store max
            score[i][j] = max(match, delete, insert)
    
    # print_matrix(score)
    
    # traceback
    
    align1 = []
    align2 = []
    i = m
    j = n

    while i > 0 and j > 0:
        score_current = score[i][j]
        score_diagonal = score[i-1][j-1]
        score_up = score[i][j-1]
        score_left = score[i-1][j]
        
        # find origin cell
        if score_current == score_diagonal + match_score(seq1[j-1], seq2[i-1]):
            align1.append(seq1[j-1])
            align2.append(seq2[i-1])
            i -= 1
            j -= 1
        elif score_current == score_up + gap_penalty:
            align1.append(seq1[j-1])
            align2.append('-')
            j -= 1
        elif score_current == score_left + gap_penalty:
            align1.append('-')
            align2.append(seq2[i-1])
            i -= 1

    # top left cell
    while j > 0:
        align1.append(seq1[j-1])
        align2.append('-')
        j -= 1
    while i > 0:
        align1.append('-')
        align2.append(seq2[i-1])
        i -= 1
    
    # reverse order
    align1 = align1[::-1]
    align2 = align2[::-1]
    
    return(align1, align2)


# ## Run

# In[2]:


import os
from os import listdir
from os.path import isfile, join

srcdir = "corpus_tsv"
dstdir = "corpus_tsv_aligned"

if not os.path.exists(dstdir):
    os.mkdir(dstdir)

files = [f for f in listdir(srcdir) if isfile(join(srcdir, f))]

for f in files:
    print(f)
    srcf = open(srcdir + '/' + f, "r", encoding="utf8")
    dstf = open(dstdir + '/' + f, "w", encoding = "utf8")

    for line in srcf.readlines():
        seqs = line.rstrip().split('\t')
        if (len(seqs) < 2):
            continue
        seq1 = seqs[0].split(' ')
        seq2 = seqs[1].split(' ')
        out1, out2 = needleman_wunsch(seq1, seq2)
        n = len(out1)
        for i in range(n):
            dstf.write(out1[i] + '\t' + out2[i] + '\n')
    dstf.close()
    srcf.close()


# In[ ]:





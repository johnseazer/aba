from ASR_metrics import utils as metrics
from itertools import product
from more_itertools import consume


# alignment

def align_words(file):

	res = []

	# init substitution matrix
	submat = init_submat_chars()

	# read file
	with open(file, 'r', encoding = 'utf8') as src:
		lines = src.readlines()

	# process lines and add to list
	for line in lines:
		# split line
		sequences = line.rstrip().split('\t')
		# ignore bad lines
		if (len(sequences) != 2):
			print(f'\tcorpus error : bad line format\t{sequences}')
			continue
		# unpack sequences
		(old, new) = sequences
		# pre-process sequences
		old = preprocess_tsv(old)
		new = preprocess_tsv(new)
		# align words with needleman-wunsch
		(old, new) = needleman_wunsch(old, new, submat = submat, mode = 'words')
		# post-process sequences
		(old, new) = align_compound_words(old, new)
		# save in list
		for (a, b) in zip(old, new):
			res.append((a, b))

	return res
		

def align_compound_words(a, b):
	'''
	aligns two same-sized lists of strings
	where compound words are formatted with '¤'
	'''
	# init result lists
	res_a = []
	res_b = []
	indexes = iter(range(len(a)))
	costs = (1, 1, 1)
	submat = init_submat_chars()

	# process lists
	for i in indexes:

		# if one of the two words from the current pair is empty :
		# both words must be respectively concatenated
		# with either their previous or next word
		if (a[i] == '¤' or b[i] == '¤'):
			
			# determine whether the concatenation must be done
			# with the previous or the next word

			if (i == 0):
				# first word pair : concatenate with next
				concatenate_with = 'next'
			elif (i == len(a) - 1):
				# last word pair : concatenate with prev
				concatenate_with = 'prev'
			
			# neither first or last word : compare distance of both options
			else:
				
				# distance when concatenating with next word
				wa = ((a[i] + ' ').strip('¤') + a[i+1]).lstrip(' ').rstrip(' ')
				wb = ((b[i] + ' ').strip('¤') + b[i+1]).lstrip(' ').rstrip(' ')
				distance_next = levenshtein(wa, wb, costs, submat)
				
				# distance when concatenating with previous word
				wa = (a[i-1] + ' ' + a[i].strip('¤')).lstrip(' ').rstrip(' ')
				wb = (b[i-1] + ' ' + b[i].strip('¤')).lstrip(' ').rstrip(' ')
				distance_prev = levenshtein(wa, wb, costs, submat)
				
				if (distance_next < distance_prev):
					concatenate_with = 'next'
				else:
					concatenate_with = 'prev'

			# concatenate and store in result
			if concatenate_with == 'next':
				wa = ((a[i] + ' ').strip('¤') + a[i+1]).lstrip(' ').rstrip(' ')
				wb = ((b[i] + ' ').strip('¤') + b[i+1]).lstrip(' ').rstrip(' ')
				a[i+1] = wa
				b[i+1] = wb
				consume(indexes, 1)
			else:
				wa = (a[i-1] + ' ' + a[i].strip('¤')).lstrip(' ').rstrip(' ')
				wb = (b[i-1] + ' ' + b[i].strip('¤')).lstrip(' ').rstrip(' ')
				res_a.pop()
				res_b.pop()

		else:
			wa = a[i]
			wb = b[i]

		res_a.append(wa)
		res_b.append(wb)

	return res_a, res_b

def align_chars(s, t, submat):
	s, t = needleman_wunsch(list(s), list(t), submat = submat)
	return ''.join(s), ''.join(t)

def needleman_wunsch(a, b, scores = (4, -1, -1), submat = {}, mode = 'word'): 
	"""Returns alignment of sequences a and b.

	:param scores: Scores for match award, mismatch penalty and gap penalty
	:type scores: tuple (match, mismatch, gap)
	"""

	# unpack score parameters
	_, _, gap_penalty = scores

	# init matrix
	rows, cols, matrix = init_matrix(a, b, factor = gap_penalty)

	# fill matrix
	for x, y in product(range(1, rows), range(1, cols)):
		# compute values from top, left, and top-left diagonal cells
		match = matrix[x-1][y-1] + score(a[x-1], b[y-1], scores, submat, mode)
		insert = matrix[x][y-1] + gap_penalty
		delete = matrix[x-1][y] + gap_penalty
		# store maxs
		matrix[x][y] = max(match, delete, insert)

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
			and current_score == topleft_score + score(a[x-1], b[y-1], scores, submat, mode)):
			# origin is top-left
			align_a.append(a[x-1])
			align_b.append(b[y-1])
			x = x-1
			y = y-1
		elif y > 0 and current_score == left_score + gap_penalty:
			# origin is left
			align_a.append('¤')
			align_b.append(b[y-1])
			y = y-1
		elif x > 0 and current_score == top_score + gap_penalty:
			# origin is top
			align_a.append(a[x-1])
			align_b.append('¤')
			x = x-1
		else:
			raise ValueError('Traceback failed')

	# reverse sequence order
	align_a = align_a[::-1]
	align_b = align_b[::-1]

	return (align_a, align_b)


def score(a, b, scores, submat, mode):
	# unpack score parameters
	match_award, mismatch_penalty, gap_penalty = scores
	# make all lowercase
	a = a.lower()
	b = b.lower()
	# match
	if (a == b
	 or a == '&' and b == 'et'):
		return match_award
	# substitution matrix
	elif (a in submat and b in submat[a]):
	  return submat[a][b]
	# gap
	elif a == '¤' or b == '¤':
		return gap_penalty
	# mismatch
	elif (mode == 'words' and len(a) >= 1 and len(b) >= 1):
		dist = levenshtein(a, b, costs = (1, 1, 2), submat = submat)
		if (dist < min(len(a), len(b)) and dist < 4):
			return match_award - dist
		else:
			return mismatch_penalty
	else:
		return mismatch_penalty


# distance

def levenshtein(a, b, costs = (1, 1, 1), submat = {}):
	"""Returns the Levensthein distance between two strings"""
	# unpack cost parameters
	del_cost, ins_cost, sub_cost = costs
	# init matrix
	rows, cols, dist = init_matrix(a, b)
	# fill matrix
	for x, y in product(range(1, rows), range(1, cols)):
		if a[x-1] == b[y-1] or a[x-1] in submat and b[y-1] in submat[a[x-1]]:
			cost = 0
		else:
			cost = sub_cost
		substitute = dist[x-1][y-1] + cost
		insert = dist[x-1][y] + ins_cost
		delete = dist[x][y-1] + del_cost
		dist[x][y] = min(substitute, insert, delete)
	return dist[x][y]


# substitution matrix

def add_to_submat(a, b, n, submat):
	if a not in submat:
		submat[a] = {b: n}
	else:
		submat[a].update({b: n})

def init_submat_chars():
	submat = {}
	# diacritics
	add_to_submat('a', 'à', 2, submat)
	add_to_submat('a', 'â', 2, submat)
	add_to_submat('â', 'a', 2, submat)
	add_to_submat('ã', 'a', 2, submat)
	add_to_submat('c', 'ç', 2, submat)
	add_to_submat('e', 'é', 2, submat)
	add_to_submat('e', 'è', 2, submat)
	add_to_submat('e', 'ê', 2, submat)
	add_to_submat('é', 'e', 2, submat)
	add_to_submat('ë', 'e', 2, submat)
	add_to_submat('ẽ', 'e', 2, submat)
	add_to_submat('i', 'î', 2, submat)
	add_to_submat('o', 'ô', 2, submat)
	add_to_submat('õ', 'o', 2, submat)
	add_to_submat('u', 'û', 2, submat)
	add_to_submat('û', 'u', 2, submat)
	add_to_submat('ü', 'u', 2, submat)
	add_to_submat('ũ', 'u', 2, submat)
	# ramist
	add_to_submat('i', 'j', 2, submat)
	add_to_submat('j', 'i', 1, submat)
	add_to_submat('u', 'v', 1, submat)
	add_to_submat('v', 'u', 1, submat)
	# replacement
	add_to_submat('c', 'q', 1, submat)
	add_to_submat('q', 'c', 1, submat)
	add_to_submat('g', 'n', 1, submat)
	add_to_submat('n', 'm', 1, submat)
	add_to_submat('s', 'z', 1, submat)
	add_to_submat('y', 'i', 2, submat)
	add_to_submat('œ', 'o', 2, submat)
	add_to_submat('o', 'œ', 2, submat)
	# old chars
	add_to_submat('&', 'e', 2, submat)
	add_to_submat('ß', 's', 2, submat)
	add_to_submat('ſ', 's', 2, submat)
	add_to_submat('ſ', 'z', 1, submat)
	return submat

def init_submat_words():
	submat = {}
	add_to_submat('&', 'et', 4, submat)
	return submat


# evaluation

def cacc(lst):
	return 1 - sum(metrics.calculate_cer(mod, new) for (mod, new) in lst) / len(lst)

def wacc(lst):
	return 1 - sum(metrics.calculate_wer(mod, new) for (mod, new) in lst) / len(lst)


# tools

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

def preprocess_tsv(s):
	s = link_hyphens(s)
	s = separate_apostrophe (s)
	s = separate_punctuation (s)
	s = s.replace("'","’")
	# split on all whitespace
	return s.split()

def link_hyphens(s):
	# TRES- CHRESTIENNE → TRES-CHRESTIENNE
	return s.replace('-', '- ')

def separate_apostrophe(s):
	return s.replace('’', '’ ').replace('\'', '\' ')

def separate_punctuation(s):
	# symbols to treat as single tokens (apostrophe and hyphen not counted)
	punctuation = '!"\\()*,./:;>?[]^«¬»„…'
	# separate these symbols in the string (add space before and after)
	for char in punctuation:
		# s = s.replace(char, ' ' + char + ' ')
		s = s.replace(char, ' ')
	# special case for ... (put consecutive periods back together)
	s = s.replace('.  .  .', '...')
	return s
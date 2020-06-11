'''
levenshtein distance

# Christopher P. Matthews
# christophermatthews1985@gmail.com
# Sacramento, CA, USA
'''

def levenshtein(s, t):
		''' From Wikipedia article ; Iterative with two matrix rows. '''
		# special cases of equivalent characters
		s = s.replace('&', 'et')
		# distance
		if s == t: return 0
		elif len(s) == 0: return len(t)
		elif len(t) == 0: return len(s)
		v0 = [None] * (len(t) + 1)
		v1 = [None] * (len(t) + 1)
		for i in range(len(v0)):
			v0[i] = i
		for i in range(len(s)):
			v1[0] = i + 1
			for j in range(len(t)):
				cost = 0 if s[i] == t[j] else 1
				v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
			for j in range(len(v0)):
				v0[j] = v1[j]           
		return v1[len(t)]

'''
needleman-wunsch algorithm

source : https://wilkelab.org/classes/SDS348/2018_spring/labs/lab13-solution.html
modified to process word sequences instead of letter sequences
'''

# scoring table
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

def match_score(a, b, distance):
	if (a == b or
		a in 'eêéè' and b in 'eêéè' or 
		distance == True and levenshtein(a, b) <= 1):
		return match_award
	elif a == '¤' or b == '¤':
		return gap_penalty
	else:
		return mismatch_penalty

def needleman_wunsch(seq1, seq2, distance = True): 
	
	# init matrix
	n = len(seq1)
	m = len(seq2)
	score = zeros(m + 1, n + 1)
	
	# fill first col
	for i in range(0, m + 1):
		score[i][0] = gap_penalty * i
	# fill first row
	for j in range(0, n + 1):
		score[0][j] = gap_penalty * j
	
	# fill all cells
	for i in range(1, m + 1):
		for j in range(1, n + 1):
			# compute values from top, left, and top-left diagonal cells
			match = score[i - 1][j - 1] + match_score(seq1[j-1], seq2[i-1], distance)
			delete = score[i - 1][j] + gap_penalty
			insert = score[i][j - 1] + gap_penalty
			# store the max of the three values
			score[i][j] = max(match, delete, insert)
 
	# init traceback
	align1 = []
	align2 = []
	i = m
	j = n

	# traceback
	while i > 0 and j > 0:
		
		# retrieve scores
		score_current = score[i][j]
		score_diagonal = score[i-1][j-1]
		score_up = score[i][j-1]
		score_left = score[i-1][j]
		
		# find the origin cell, store corresponding elements, and advance
		if score_current == score_diagonal + match_score(seq1[j-1], seq2[i-1], distance):
			# origin is top-left diagonal
			align1.append(seq1[j-1])
			align2.append(seq2[i-1])
			i -= 1
			j -= 1
		elif score_current == score_up + gap_penalty:
			# origin is top
			align1.append(seq1[j-1])
			align2.append('¤')
			j -= 1
		elif score_current == score_left + gap_penalty:
			# origin is left
			align1.append('¤')
			align2.append(seq2[i-1])
			i -= 1

	# proceed to topmost leftmost cell
	while j > 0:
		align1.append(seq1[j-1])
		align2.append('¤')
		j -= 1
	while i > 0:
		align1.append('¤')
		align2.append(seq2[i-1])
		i -= 1
	
	# reverse the elements order
	align1 = align1[::-1]
	align2 = align2[::-1]
	
	return(align1, align2)

'''
pre-processing
'''

def preprocess(s):
	s = link_hyphens(s)
	s = separate_apostrophe (s)
	s = separate_punctuation (s)
	# split on all whitespace
	return s.split()

def link_hyphens(s):
	# TRES- CHRESTIENNE → TRES-CHRESTIENNE
	return s.replace('- ', '-')

def separate_apostrophe(s):
	return s.replace('’', '’ ').replace('\'', '\' ')

def separate_punctuation(s):
	# symbols to treat as single tokens (apostrophe and hyphen not counted)
	punctuation = '!"\()*,./:;>?[]^«¬»„…'
	# separate these symbols in the string (add space before and after)
	for char in punctuation:
		s = s.replace(char, ' ' + char + ' ')
	# special case for ... (put consecutive periods back together)
	s = s.replace('.  .  .', '...')
	return s

def align_compound_words(a, b):
	
	'''
	aligns two same-sized lists of strings
	where compound words are formatted with '¤'
	
	['Ie', 'poſſede', 'quatre', 'vingt',    'dix',              'pieces']
	['Je', 'possède', '¤',      '¤',        'quatre-vingt-dix', 'pièces']
	→
	['Ie', 'poſſede', 'quatre vingt dix', 'pieces']
	['Je', 'possède', 'quatre-vingt-dix', 'pièces']
	'''
	
	# init result lists
	res_a = []
	res_b = []
	
	# for each word pair
	for i in range(len(a)):

		# alias for current words
		wa = a[i]
		wb = b[i]
		
		# one of the words has '¤' as first and last char → part of compound
		# ('¤' as first char but not last → end of compound)
		if (wa[0] == '¤' and wa[-1] == '¤' or
			wb[0] == '¤' and wb[-1] == '¤'):
			
			# i+1 out of range → error from before : print and ignore
			if len(a) == i+1 and len(b) == i+1:
				print('\terror : compound but no next word')
				print('\t\t' + str(a))
				print('\t\t' + str(b))
				continue

			# both words : add a space, and add as a prefix before next word 
			a[i+1] = wa + ' ' + a[i+1]
			b[i+1] = wb + ' ' + b[i+1]      

			# processing is delegated to next word pair so ignore current word
			continue
		
		# else → end of compound or regular word pair
		else:
			# strip processing chars in case of end of compund
			wa = wa.lstrip('¤ ')
			wb = wb.lstrip('¤ ')
			# append to result sequences
			res_a.append(wa)
			res_b.append(wb)
	# return result lists
	return res_a, res_b

def align_chars(s, t):
	s, t = needleman_wunsch(list(s), list(t), distance = False)
	return ''.join(s), ''.join(t)

def has_diff(str1, str2, seq1, seq2):
	'''
	returns true if both strings contain respective sequence at same index
	'''
	assert len(str1) == len(str2), 'error : words not aligned'
	return True if (str1.find(seq1) == str2.find(seq2)) else False

def get_diffs(a, b):

	'''
	returns the list of differences between strings a and b
	format : (old_chars, new_chars, rule_applied)
	'''
	res = []
	
	# for each char
	for i in range(len(a)):
		
		# check if diff
		if a[i] != b[i]:
			
			# search 1 char diff
			old = a[i]
			new = b[i]
			
			# s long
			if (old, new) == ('ſ', 's'):
				res.append((old, new, 's long'))
			# accents
			elif (old, new) == ('e', 'é'):
				res.append((old, new, 'accent'))
			# apostrophe
			elif (old, new) == ("'", "’"):
				res.append((old, new, 'apostrophe'))
			
			# search 2 char diff
			elif (i+1 < len(a)):
				old = a[i:i+2]
				new = b[i:i+2]

				# ampersand
				if (old == '¤&' and new == 'et'):
					res.append((old, new, 'esperluette'))

				# double consonant
				if (old[0] == '¤' and new[0] == new[1] == old[1]):
					res.append((old, new, 'double consonne'))

	# return list of all diffs
	return res

def pairs_to_file(a, b, dst, delta_only = False):
	'''
	takes two same-sized lists of strings a and b
	writes each pair of corresponding strings as a line to dst in tsv format
	'''
	assert len(a) == len(b), 'different list sizes'
	# go through each pair of corresponding words
	for old, new in zip(a, b):
		# ignore pairs of identical words if delta only
		if (delta_only and old == new):
			continue
		# write pair of corresponding words to file in tsv format
		dst.write(old + '\t' + new + '\n')

def pair_to_dic(old, new, dic, delta_only = False):
	
	'''
	takes two strings old and new
	adds the pair to dictionary dic as follows :
	- keys are strings from old
	- values are dictionaries in which :
		- keys are strings from new
		- values are the count of (old, new) occurences
	'''

	# delta only : ignore identical words
	if (delta_only and old == new):
		return
	# pair already in dic : increment count
	if old in dic and new in dic[old]:
		dic[old][new] += 1
	# pair not in dic : add to dic
	else:
		dic[old] = {new: 1}

def dic_to_file(dic, f):
	'''
	write dictionary to tsv
	format : old, new, count
	'''
	for old in dic:
		for new in dic[old]:
			count = dic[old][new]
			f.write(old + '\t' + new + '\t' + str(count) + '\n')
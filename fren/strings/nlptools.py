from more_itertools import consume
from .alignment import needleman_wunsch
from .distance import levenshtein
from .substitution import init_submat_chars

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

			# first word pair : concatenate with next
			if (i == 0):
				concatenate_with = 'next'
			# last word pair : concatenate with prev
			elif (i == len(a) - 1):
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

def find_diffs(old, new):

	assert len(old) == len(new), 'error : words not aligned'

	diffs = []

	# todo : treat maj
	old = old.lower()
	new = new.lower()

	indexes = iter(range(len(old)))

	for i in indexes:

		if old[i] != new[i]:

			if (old[i] == new[i].upper() or
				new[i] == old[i].upper()):
				diffs.append((old[i], new[i], ['majuscule']))
			if (old[i] == 'ſ' and
				new[i] in 'sz'):
				diffs.append((old[i], new[i], ['s long']))

			# ocr errors
			elif (old[i] in 'lf' and new[i] in 's'
			 or old[i] in 'ſ' and new[i] in 'lf'
			 or old[i] in 'r' and new[i] in 't'
			 or old[i] in 'n' and new[i] in 'r'
			 or old[i] in 'i' and new[i] in 'l'
			 or old[i] == 'u' and new[i] == 'n'
			 or old[i] == 'l' and new[i] in 'ij'):
				diffs.append((old[i], new[i], ['ocr error']))

			elif (old[i-3:i+1] == 'oing' and new[i-3:i+1] == 'oin¤'):
				diffs.append((old[i-3:i+1], new[i-3:i+1], ['oing → oin']))

			elif (old[i:i+3] == 'ain' and new[i:i+3] == 'ein'):
				diffs.append((old[i:i+3], new[i:i+3], ['ain ↔ ein']))
				consume(indexes, 2)

			# eoi → oi
			elif (old[i:i+3] == 'eoi' and new[i:i+3] == '¤oi'):
				diffs.append((old[i:i+3], new[i:i+3], ['eoi → oi']))
				consume(indexes, 2)

			# ein → in
			elif (old[i:i+3] == 'ein' and new[i:i+3] == '¤in'):
				diffs.append((old[i:i+3], new[i:i+3], ['ein → in']))
				consume(indexes, 2)

			# eil → il
			elif (old[i:i+3] == 'eil' and new[i:i+3] == '¤il'):
				diffs.append((old[i:i+3], new[i:i+3], ['eil → il']))
				consume(indexes, 2)

			# nn → mn
			elif (old[i:i+2] == 'nn' and new[i:i+2] == 'mn'):
				diffs.append((old[i:i+2], new[i:i+2], ['nn → mn']))
				consume(indexes, 1)

			# mt/nt → mpt
			elif (old[i:i+3] in ['n¤t','¤nt'] and new[i:i+3] == 'mpt'):
				diffs.append((old[i:i+3], new[i:i+3], ['mt/nt → mpt']))
				consume(indexes, 2)
			elif (old[i-1:i+2] == 'm¤t' and new[i-1:i+2] == 'mpt'):
				diffs.append((old[i-1:i+2], new[i-1:i+2], ['mt/nt → mpt']))
				consume(indexes, 1)

			# ept → et / ipt → it / opc → oc
			elif (old[i-1:i+2] == 'ept' and new[i-1:i+2] == 'e¤t'
			   or old[i-1:i+2] == 'ipt' and new[i-1:i+2] == 'i¤t'
			   or old[i-1:i+2] == 'opc' and new[i-1:i+2] == 'o¤c'):
				diffs.append((old[i-1:i+2], new[i-1:i+2], ['suppression lettre étymologique']))

			# latin eus/us → e
			elif (old[i:i+3] == 'eus' and new[i:i+3] == 'e¤¤'):
				diffs.append((old[i:i+3], new[i:i+3], ['terminaison latine us → e']))
				consume(indexes, 2)
			elif (old[i:i+2] == 'us' and new[i:i+2] in ['e¤','¤e']):
				diffs.append((old[i:i+2], new[i:i+2], ['terminaison latine us → e']))
				consume(indexes, 1)

			# au → eau
			elif (old[i:i+3] == '¤au' and new[i:i+3] == 'eau'):
				diffs.append((old[i:i+3], new[i:i+3], ['au → eau']))
				consume(indexes, 2)

			# cque/que → c (avecques, avecque, aveque)
			elif (i-1 > 0 and old[i-1] == new[i-1] == 'c'
				and old[i:i+4] == 'ques' and new[i:i+4] == '¤¤¤¤'):
				diffs.append((old[i:i+4], new[i:i+4], ['cque/que → c']))
				consume(indexes, 3)

			elif (old[i:i+3] == 'que' and new[i:i+3] == 'c¤¤'):
				diffs.append((old[i:i+3], new[i:i+3], ['cque/que → c']))
				consume(indexes, 2)

			elif (i-1 > 0 and old[i-1] == new[i-1] == 'c'
				and old[i:i+3] == 'que' and new[i:i+3] == '¤¤¤'):
				diffs.append((old[i:i+3], new[i:i+3], ['cque/que → c']))
				consume(indexes, 2)

			# séparation
			elif (old[i:i+2] == '¤¤' and new[i:i+2] in ["' ", "’ "]):
				diffs.append((old[i:i+2], new[i:i+2], ['séparation avec apostrophe']))
				consume(indexes, 1)

			elif (old[i:i+2] in ['œ¤','¤œ'] and new[i:i+2] == 'oe'
			   or old[i:i+2] == 'oe' and new[i:i+2] in ['œ¤','¤œ']):
				diffs.append((old[i:i+2], new[i:i+2], ['œ ↔ oe']))
				consume(indexes, 1)

			elif (old[i:i+2] in ["' ", "’ "] and new[i:i+2] == '¤¤'):
				diffs.append((old[i:i+2], new[i:i+2], ['contraction']))
				consume(indexes, 1)

			elif (old[i:i+2] in ['ai','ei'] and new[i:i+2] in ['è¤','¤è', 'e¤','¤e']):
				diffs.append((old[i:i+2], new[i:i+2], ['ai/ei → e/è']))
				consume(indexes, 1)

			elif (old[i:i+2] == 'an' and new[i:i+2] == 'en'
			   or old[i:i+2] == 'en' and new[i:i+2] == 'an'
			   or old[i:i+2] == 'am' and new[i:i+2] == 'em'
			   or old[i:i+2] == 'em' and new[i:i+2] == 'am'):
				diffs.append((old[i:i+2], new[i:i+2], ['an/am ↔ en/em']))
				consume(indexes, 1)

			elif (old[i:i+2] == 'gd' and new[i:i+2] == '¤d'):
				diffs.append((old[i:i+2], new[i:i+2], ['gd → d']))
				consume(indexes, 1)

			elif (old[i:i+2] == 'ct' and new[i:i+2] == '¤t'):
				diffs.append((old[i:i+2], new[i:i+2], ['ct → t']))
				consume(indexes, 1)

			elif (old[i:i+2] == 'nt' and new[i:i+2] == 'mt'):
				diffs.append((old[i:i+2], new[i:i+2], ['nt → mt']))
				consume(indexes, 1)

			elif (old[i:i+2] == 'qu' and new[i:i+2] in ['¤c', 'c¤']
			   or old[i:i+2] in ['¤c', 'c¤'] and new[i:i+2] == 'qu'):
				diffs.append((old[i:i+2], new[i:i+2], ['qu ↔ c']))
				consume(indexes, 1)

			elif (old[i:i+2] in ['¤f', 'f¤'] and new[i:i+2] == 'ph'):
				diffs.append((old[i:i+2], new[i:i+2], ['f → ph']))
				consume(indexes, 1)

			# as → â
			elif (old[i:i+2] in ['aſ','as'] and new[i:i+2] == 'â¤'):
				diffs.append((old[i:i+2], new[i:i+2], ['as → â']))
				consume(indexes, 1)

			# es → é
			elif (old[i:i+2] in ['eſ','es'] and new[i:i+2] == 'é¤'):
				diffs.append((old[i:i+2], new[i:i+2], ['es → é']))
				consume(indexes, 1)

			# double consonne avec s long
			elif (old[i:i+2] in ['ſ¤','¤ſ'] and new[i:i+2] == 'ss'):
				diffs.append((old[i:i+2], new[i:i+2], ['double consonne']))
				consume(indexes, 1)

			elif (old[i-1:i+1] in ['ul', 'il'] and new[i-1:i+1] in ['i¤', 'u¤']):
				diffs.append((old[i-1:i+1], new[i-1:i+1], ['suppression l après voyelle']))

			elif (old[i:i+2] == 'ph' and new[i:i+2] in ['¤f', 'f¤']):
				diffs.append((old[i:i+2], new[i:i+2], ['ph → f']))
				consume(indexes, 1)

			elif (old[i:i+2] in ['¤o', 'o¤'] and new[i:i+2] == 'au'
			   or old[i:i+2] == 'au' and new[i:i+2] in ['¤o', 'o¤']):
				diffs.append((old[i:i+2], new[i:i+2], ['o ↔ au']))
				consume(indexes, 1)

			elif (old[i:i+2] in ['&¤','¤&'] and
				  new[i:i+2] == 'et'):
				diffs.append((old[i:i+2], new[i:i+2], ['esperluette']))
				consume(indexes, 1)
			elif (old[i:i+2] in ['ß¤','¤ß'] and
				  new[i:i+2] == 'ss'):
				diffs.append((old[i:i+2], new[i:i+2], ['eszett']))
				consume(indexes, 1)
			elif (old[i:i+2] in ['eu','eû', 'ev', 'eü'] and
				  new[i:i+2] in ['¤u', '¤û']):
				diffs.append((old[i:i+2], new[i:i+2], ['eu → u']))
				consume(indexes, 1)
			elif (old[i:i+2] == 'y¤' and
				  new[i:i+2] == 'is'):
				diffs.append((old[i:i+2], new[i:i+2], ['terminaison y → is']))
				consume(indexes, 1)
			elif (old[i:i+2] == 'lt' and
				  new[i:i+2] == '¤t'):
				diffs.append((old[i:i+2], new[i:i+2], ['voyelle + lt → voyelle + t']))
				consume(indexes, 1)
			elif (old[i:i+2] == 'gn' and
				  new[i:i+2] == 'nn'):
				diffs.append((old[i:i+2], new[i:i+2], ['gn → nn']))
				consume(indexes, 1)
			elif (old[i:i+2] == 'es' and
				  new[i:i+2] in ["¤'", "¤’", "'¤", "’¤"]):
				diffs.append((old[i:i+2], new[i:i+2], ['élision es → apostrophe']))
				consume(indexes, 1)

			# tilde
			elif (old[i:i+2] in ['ã¤','¤ã'] and new[i:i+2] in ['am','an']
			   or old[i:i+2] in ['ẽ¤','¤ẽ'] and new[i:i+2] in ['em','en']
			   or old[i:i+2] in ['õ¤','¤õ','ō¤','¤ō'] and new[i:i+2] in ['om','on']
			   or old[i:i+2] in ['ũ¤','¤ũ'] and new[i:i+2] in ['um','un']):
				diffs.append((old[i:i+2], new[i:i+2], ['tilde → voyelle + m/n']))
				consume(indexes, 1)
			elif (old[i:i+2] in ['sc', 'sç', 'ſc', 'ſç'] and new[i:i+2] == 's¤'):
				diffs.append((old[i:i+2], new[i:i+2], ['sc → s']))
				consume(indexes, 1)

			# double consonne
			elif (i+1 < len(old) and
				 (old[i] == '¤' and old[i+1] == new[i] == new[i+1]
				or new[i] == '¤' and new[i+1] == old[i] == old[i+1])):
				diffs.append((old[i:i+2], new[i:i+2], ['double consonne']))
				consume(indexes, 1)
			elif (i-1 > 0 and 
				(old[i] == '¤' and old[i-1] == new[i] == new[i-1]
				or new[i] == '¤' and new[i-1] == old[i] == old[i-1])):
				diffs.append((old[i:i+2], new[i:i+2], ['double consonne']))
			
			elif ((old[i], new[i]) == ('c', 'ç') or
				  (old[i], new[i]) == ('ç', 'c')):
				diffs.append((old[i], new[i], ['cédille']))
			elif (old[i] == 'y' and
				  new[i] in ['i', 'ï']):
				diffs.append((old[i], new[i], ['lettre calligraphique']))
			elif (old[i] in ['i', 'ï'] and
				  new[i] == 'y'):
				diffs.append((old[i], new[i], ['i → y']))
			elif (old[i] in ['x', 'z'] and
				  new[i] == 's'):
				diffs.append((old[i], new[i], ['x/z → s']))
			elif (old[i] == 'c' and
				  new[i] == 's'):
				diffs.append((old[i], new[i], ['c → s']))
			elif (old[i] in 'sſ' and
				  new[i] == 'z'):
				diffs.append((old[i], new[i], ['s → z']))
			elif (old[i] in 'sſ' and
				  new[i] == 't'):
				diffs.append((old[i], new[i], ['s → t']))
			elif (old[i] in 'sſ' and
				  new[i] == 'c'):
				diffs.append((old[i], new[i], ['s → c']))
			elif (old[i] == 'd' and
				  new[i] == 't'):
				diffs.append((old[i], new[i], ['d → t']))
			elif (old[i] == 't' and
				  new[i] == 'd'):
				diffs.append((old[i], new[i], ['t → d']))
			elif (old[i] == 'o' and
				  new[i] == 'a'):
				diffs.append((old[i], new[i], ['o → a']))
			
			elif (old[i] in "'’" and new[i] == 'e'):
				diffs.append((old[i], new[i], ['apostrophe → e']))

			# o → œ
			elif (old[i] == 'o' and new[i] == 'œ'):
				diffs.append((old[i], new[i], ['o → œ']))

			# æ/œ
			elif (old[i] == 'æ' and new[i] in 'eé'):
				diffs.append((old[i], new[i], ['æ → e']))
			elif (old[i] == 'œ' and new[i] in 'eé'):
				diffs.append((old[i], new[i], ['œ → e']))
			
			elif (old[i] == '¤' and
				  new[i] == 'h'):
				diffs.append((old[i], new[i], ['ajout h mot grec']))
			elif (old[i] in 'aàâ' and new[i] in 'aàâ'
				or old[i] in 'EÉÈÊË' and new[i] in 'EÉÈÊË'
				or old[i] in 'eéèêë' and new[i] in 'eéèêë'
				or old[i] in 'iîï' and new[i] in 'iîï'
				or old[i] in 'oõô' and new[i] in 'oõô'
				or old[i] in 'uùûü' and new[i] in 'uùûü'):
				diffs.append((old[i], new[i], ['accent']))
			elif (old[i] in ["'", "’"] and
				  new[i] in ["'", "’"]):
				diffs.append((old[i], new[i], ['apostrophe']))
			elif (old[i] in [' ', '-'] and
				  new[i] in ['-', '¤']):
				diffs.append((old[i], new[i], ['fusion']))
			elif (old[i] in ['¤', '-'] and
				  new[i] in ['-', ' ']):
				diffs.append((old[i], new[i], ['séparation']))
			elif (old[i] == '¤' and
				  new[i] in ['d', 't']):
				diffs.append((old[i], new[i], ['ajout d/t terminaison']))
			elif (old[i] in 'uv' and
				  new[i] in 'vu' or
				  old[i] in 'ij' and
				  new[i] in 'ij'):
				diffs.append((old[i], new[i], ['lettre ramiste']))
			elif (old[i] in 'ſshtdcçb' and new[i] == '¤'):
				diffs.append((old[i], new[i], ['suppression lettre étymologique']))
			# no rule found
			else:
				diffs.append((old[i], new[i], []))

	return len(diffs), diffs

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
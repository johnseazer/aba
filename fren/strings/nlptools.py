from more_itertools import consume
from .alignment import needleman_wunsch

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

			# auecque/avecque, doncque
			elif (i-1 > 0 and old[i-1] == new[i-1] == 'c'
				and old[i:i+4] == 'ques' and new[i:i+4] == '¤¤¤¤'):
				diffs.append((old[i:i+4], new[i:i+4], ['avecque(s)/doncque(s)']))
				consume(indexes, 3)
			elif (i-1 > 0 and old[i-1] == new[i-1] == 'c'
				and old[i:i+3] == 'que' and new[i:i+3] == '¤¤¤'):
				diffs.append((old[i:i+3], new[i:i+3], ['avecque(s)/doncque(s)']))
				consume(indexes, 2)

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
			   or old[i:i+2] in ['õ¤','¤õ'] and new[i:i+2] in ['om','on']
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
			elif (old[i] == 's' and
				  new[i] == 'z'):
				diffs.append((old[i], new[i], ['s → z']))
			elif (old[i] == 's' and
				  new[i] == 't'):
				diffs.append((old[i], new[i], ['s → t']))
			elif (old[i] == 'd' and
				  new[i] == 't'):
				diffs.append((old[i], new[i], ['d → t']))
			elif (old[i] == 't' and
				  new[i] == 'd'):
				diffs.append((old[i], new[i], ['t → d']))
			elif (old[i] == 'o' and
				  new[i] == 'a'):
				diffs.append((old[i], new[i], ['o → a']))
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
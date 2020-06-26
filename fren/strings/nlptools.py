from .needlemanwunsch import align

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
	s, t = align(list(s), list(t))
	return ''.join(s), ''.join(t)

def has_diff(str1, str2, seq1, seq2):
	'''
	returns true if both strings contain respective sequence at same index
	'''
	assert len(str1) == len(str2), 'error : words not aligned'
	return True if (str1.find(seq1) == str2.find(seq2)) else False

def get_diffs(string1, string2):

	'''
	returns the number and list of changes between strings a and b
	format : (substring1, substring2, applied_rules)
	'''
	assert len(string1) == len(string2), f'error: different size for strings ({string1} → {string2})'

	# init changes and substrings
	nchanges, changes = (0, [])
	substring1, substring2 = ('', '')

	# look at each pair of chars
	for char1, char2 in zip(string1, string2):		
		
		# if different chars
		if char1 != char2:
			
			# increment change counter
			nchanges += 1
			# add chars to substrings
			substring1 += char1
			substring2 += char2
			# search for rules
			rules = find_rules(substring1, substring2)
			
			# rules found
			if rules != []:
				# add entry
				changes.append((substring1, substring2, rules))
				# reset substrings
				substring1, substring2 = ('', '')
		
		# if same char but diff exists
		elif len(substring1) > 0:
			# look for double consonant
			if (substring1 == '¤' and substring2 == char1 == char2
					or substring2 == '¤' and substring1 == char1 == char2):
				substring1 += char1
				substring2 += char2
			# find rules
			rules = find_rules(substring1, substring2)
			# add entry even if no rule found
			changes.append((substring1, substring2, rules))
			# reset substrings
			substring1, substring2 = ('', '')

	# end of strings : if current substrings
	if substring1 and substring2:
		# find rules
		rules = find_rules(substring1, substring2)
		# add entry even if no rule found
		changes.append((substring1, substring2, rules))

	# return list of changes
	return nchanges, changes

def find_rules(old, new):

	assert len(old) == len(new), f'error: different size for diff ({old} → {new})'
	
	# init rules
	rules = []
	
	# 1 char rules
	if len(old) == 1:
		# majuscule
		if (new == old.lower()
				or new == old.upper()):
			rules.append('majuscule')
		else:
			# make all lowercase
			old = old.lower()
			new = new.lower()
		# s long
		if (old, new) == ('ſ', 's'):
			rules.append ('s long')
		# sç → s
		elif (old, new) == ('ç', 's'):
			rules.append ('sç → s')
		# cédille
		elif ((old, new) == ('c', 'ç')
				or (old, new) == ('ç', 'c')):
			rules.append ('cédille')
		# lettre calligraphique
		elif (old, new) == ('y', 'i'):
			rules.append ('lettre calligraphique')
		# ï → y
		elif ((old, new) == ('i', 'y')
				or (old, new) == ('ï', 'y')):
			rules.append ('ï devient y')
		# x/z → s
		elif ((old, new) == ('z', 's')
				or (old, new) == ('x', 's')):
			rules.append ('x/z devient s')
		# s → z (assés → assez) 
		elif ((old, new) == ('s', 'z')):
			rules.append ('terminaison s → z')
		# participe présent s → t
		elif ((old, new) == ('s', 't')):
			rules.append ('participe présent s → t')
		# d → t  (quand → quant)
		elif ((old, new) == ('d', 't')):
			rules.append ('terminaison d → t')
		# d → t  (étandart → étandard)
		elif ((old, new) == ('t', 'd')):
			rules.append ('terminaison t → d')
		# conjugaison
		elif (old, new) == ('o', 'a'):
			rules.append ('conjugaison')
		# accents
		elif (old in 'aàâ' and new in 'aàâ'
				or old in 'EÉÈÊË' and new in 'EÉÈÊË'
				or old in 'eéèêë' and new in 'eéèêë'
				or old in 'iîï' and new in 'iîï'
				or old in 'oô' and new in 'oô'
				or old in 'uùûü' and new in 'uùûü'):
			rules.append('accent')
		# apostrophe
		elif (old, new) == ("'", "’"):
			rules.append('apostrophe')
		# fusion de deux mots
		elif ((old, new) == (' ', '¤')
				or (old, new) == (' ', '-')
				or (old, new) == ('-', '¤')):
			rules.append ('fusion')
		# séparation de deux mots
		elif ((old, new) == ('¤', ' ')
				or (old, new) == ('-', ' ')
				or (old, new) == ('¤', '-')):
			rules.append ('séparation')
		# ajout t/d terminaison
		elif ((old, new) == ('¤', 'd')
				or (old, new) == ('¤', 't')):
			rules.append ('ajout d/t terminaison')
		# ajout d'un h pour les mots grecs
		elif ((old, new) == ('¤', 'h')):
			rules.append('ajout h mot grec')
		elif ((old, new) == ('a', 'e')):
			rules.append ('a devient e')
		# lettre ramiste
		elif ((old, new) == ('u', 'v')
				or (old, new) == ('v', 'u')
				or (old, new) == ('i', 'j')
				or (old, new) == ('j', 'i')):
			rules.append('lettre ramiste')
		# suppression lettre étymologique
		elif (old in 'ſshtdcçb' and new == '¤'):
			rules.append ('supp. lettre étymologique')

	# 2 chars rules
	elif len(old) == 2:
		# ampersand
		if (old == '¤&' and new == 'et'):
			rules.append('esperluette')
		# eu → ¤û
		if (old == 'eu' and new == '¤û'
				or old == 'eû' and new == '¤u'
				or old == 'ev' and new == '¤u'):
			rules.append('eu → u')
		# tilde
		if (old == '¤ẽ' and new == 'en'
				or old == '¤ã' and new == 'an'):
			rules.append('tilde → en/an')
		# jusques → jusqu'
		elif (old, new) == ('es', '¤’'):
			rules.append ('élision ques → qu')
		# double consonant
		elif (old[0] == '¤' and new[0] == new[1] == old[1]
				or new[0] == '¤' and old[0] == old[1] == new[1]):
			rules.append('double consonne')
	return rules

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
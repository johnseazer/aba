# modern.py

from more_itertools import consume
from .strings import init_submat_chars, align_chars

import re


def label_dic(input_file, output_file):

	submat = init_submat_chars()

	# read entries from source dictionary
	with open(f'{input_file}', 'r', encoding = 'utf8') as src:
		lines = src.readlines()
	# process entries
	with open(f'{output_file}', 'w', encoding = 'utf8') as dst:
		# process dictionary entries
		for line in lines:
			# parse entry
			old, new, count = line.rstrip('\n').split('\t')
			# align chars
			old, new = align_chars(old, new, submat = submat)
			# find differences
			ndiffs, diffs = find_diffs(old, new)
			# write new entry for each diff
			for diff in diffs:
				old_chars, new_chars, rules = diff
				dst.write(f'{old}\t{new}\t{count}\t{ndiffs}\t{old_chars}\t{new_chars}\t{rules}\n')


def preprocess(s):
	# separate and unify apostrophes
	s = re.sub(r"(['’])", r"’ ", s)
	# separate punctuation
	s = re.sub(r"([.,!?;:])", r" \1", s)
	# separate tags
	s = re.sub(r'(<.*>)', r' \1 ', s)
	return s

def postprocess(s):
	# opening tag
	s = re.sub(r'(<[^/].*>)', r' \1', s)
	# closing tag
	s = re.sub(r'(</.*>)', r'\1 ', s)
	# spaces
	s = re.sub(r' +', ' ', s)
	# punctuation
	s = re.sub(r"(['’]) ", r"'", s)
	s = re.sub(r" ([.,])", r"\1", s)
	return s

def modernize_sentence(s, modern_dic, learn_dic, name_dic = {}):
	s = preprocess(s)
	tokens_old = s.replace("'", "’").replace("’", "’ ").split(' ')
	tokens_new = [modernize(token, modern_dic, learn_dic, name_dic = name_dic) for token in tokens_old]
	s = ' '.join(tokens_new)
	s = postprocess(s)
	return s


def modernize(word, modern_dic, learning_dic, name_dic = {}, rules = True):
	# word present in modern dic : keep
	if (word and word[0].isupper() and word.replace("’", "'") in name_dic) or word.lower().replace("’", "'") in modern_dic:
		pass
	# word present in learning dic : apply learning dic
	elif word in learning_dic:
		word = learning_dic[word]
	# word absent in both dics : apply rules
	elif rules:
		mods = apply_rules(word)
		# check all modernizations
		# keep the one that appears in modern dic
		word = mods[0]
		for m in mods:
			if (m and m[0].isupper() and m.replace("’", "'") in name_dic) or m.lower().replace("’", "'") in modern_dic:
				word = m
				break
		# store result
	return word


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
			elif (old[i] in 'uv' and new[i] in 'uv' or
				  old[i] in 'ij' and new[i] in 'ij'):
				diffs.append((old[i], new[i], ['lettre ramiste']))
			elif (old[i] in 'ſshtdcçb' and new[i] == '¤'):
				diffs.append((old[i], new[i], ['suppression lettre étymologique']))
			# no rule found
			else:
				diffs.append((old[i], new[i], []))

	return len(diffs), diffs


def apply_rules(s):

	mods = []

	# s long
	s = s.replace('ſ','s')
	# eszett
	s = s.replace('ß','ss')
	# esperluette
	s = s.replace('&','et')

	# tilde
	s = s.replace('ãm','amm')
	s = s.replace('ãn','ann')
	s = s.replace('ã','an')
	s = s.replace('ẽm','emm')
	s = s.replace('ẽn','enn')
	s = s.replace('ẽ','en')
	s = s.replace('õm','omm')
	s = s.replace('õn','onn')
	s = s.replace('õ','on')
	
	# scavoir
	s = re.sub(r'^([Ss])[CÇcç]', r'\1', s)
	s = re.sub(r'^scau', r'sau', s)

	# terminaison oing
	s = re.sub(r'oing$', 'oin', s)

	# terminaison y
	s = re.sub(r'y$','i', s)

	# sch
	s = s.replace('sch','ch')

	
	s = re.sub(r'([ao])ye$', r'\1ie', s)

	mods.append(s)

	# suppression c étymologique
	if 'ct' in s:
		mods.append(s.replace('ct', 't'))

	# suppression d étymologique
	if re.search(r'[aeiou]dv', s):
		mods.append(re.sub(r'([aeiou])dv', r'\1v', s))

	# ajout d'un t ou d final (presens → présents)
	if re.search(r'[ae]ns$', s):
		mods.append(re.sub(r'([ae])ns$', r'\1nts', s))
		mods.append(re.sub(r'([ae])ns$', r'\1nds', s))

	# terminaison de verbe
	if re.search(r'(.{2,})oi([est])', s):
		mods.append(re.sub(r'(.{2,})oi([st])$', r'\1ai\2', s))
		mods.append(re.sub(r'(.{2,})oient$', r'\1aient', s))

	if re.search(r'e[Zz]$', s):
		mods.append(re.sub(r'e[Zz]$', 'és', s))

	if re.search(r'és$', s):
		mods.append(re.sub(r'és$', 'ez', s))

	if re.search(r'[aeiou]s[mnqt]', s, flags = re.IGNORECASE):
		mods.append(s.replace('st', 't'))
		mods.append(s.replace('est', 'ét'))
		# try ast → ât
		s2 = s
		s2 = re.sub(r'as([mnqt])', r'â\1', s2)
		s2 = re.sub(r'es([mnqt])', r'ê\1', s2)
		s2 = re.sub(r'is([mnqt])', r'î\1', s2)
		s2 = re.sub(r'os([mnqt])', r'ô\1', s2)
		s2 = re.sub(r'us([mnqt])', r'û\1', s2)
		mods.append(s2)
		# try est → ét
		s3 = s
		s3 = re.sub(r'es([mnqt])', r'é\1', s3)
		s3 = re.sub(r'Es([mnqt])', r'É\1', s3)
		mods.append(s3)

	if 'y' in s:
		mods.append(s.replace('y', 'i'))

	if 'ü' in s:
		mods.append(s.replace('ü', 'u'))
		mods.append(s.replace('eü', 'u'))

	# lettres ramistes, accents
	for mod in mods.copy():
		if 'is' in s:
			mods.append(mod.replace('is', 'î'))
		if 'ai' in s:
			mods.append(mod.replace('ai', 'aî'))
		if 'u' in mod:
			mods.append(mod.replace('u', 'v'))
		if 'v' in mod:
			mods.append(mod.replace('v', 'u'))
		if 'e' in mod:
			mods.append(re.sub(r'e([^$(s$)])', r'é\1', mod))

	return mods
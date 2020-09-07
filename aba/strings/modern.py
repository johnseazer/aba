# modern.py

# graph analyses
# ct

import re

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

def modernize_sentence(s, modern_dic, learn_dic):
	s = preprocess(s)
	tokens_old = s.split(' ')
	tokens_new = [modernize(token, modern_dic, learn_dic) for token in tokens_old]
	s = ' '.join(tokens_new)
	s = postprocess(s)
	return s

def modernize(word, modern_dic, learning_dic, rules = True):
	# word present in modern dic : keep
	if word.lower().replace("’", "'") in modern_dic:
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
			if m.lower() in modern_dic:
				word = m
				break
		# store result
	return word


def apply_rules(s):

	mods = []

	# caractères anciens
	s = s.replace('ſ','s')
	s = s.replace('ß','ss')
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
	
	# terminaison de verbe
	s = re.sub(r'(.{2,})oi([st])$', r'\1ai\2', s)
	s = re.sub(r'(.{2,})oient$', r'\1aient', s)
	
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

	# ajout d'un t ou d final (presens → présents)
	if re.search(r'[ae]ns$', s):
		mods.append(re.sub(r'([ae])ns$', r'\1nts', s))
		mods.append(re.sub(r'([ae])ns$', r'\1nds', s))

	if re.search(r'e[Zz]$', s):
		mods.append(re.sub(r'e[Zz]$', 'és', s))

	if re.search(r'és$', s):
		mods.append(re.sub(r'és$', 'ez', s))

	if 'st' in s:
		mods.append(s.replace('st', 't'))
		mods.append(s.replace('est', 'ét'))
		# try ast → ât
		s2 = s
		s2 = s2.replace('ast', 'ât')
		s2 = s2.replace('est', 'êt')
		s2 = s2.replace('ist', 'ît')
		s2 = s2.replace('ost', 'ôt')
		s2 = s2.replace('ust', 'ût')		
		mods.append(s2)

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
			mods.append(mod.replace('e', 'é'))

	# est → ét
	# asmes → âmes
	# evesque
	return mods
import re
import glob

from ASR_metrics import utils as metrics
from .strings.nlptools import align_chars
from .strings.substitution import init_submat_chars
from .strings.nlptools import find_diffs
from .data.saving import lst_to_tsv


def run():

	# parameters
	ratio 		= 0.6

	# paths
	modern 		= 'data/dic_morphalou.tsv'
	wiki 		= 'data/dic_wikisource.tsv'
	corpus 		= 'data/PARALLEL17_aligned'
	result_base = 'result/modernized_baseline.tsv'
	result_rule = 'result/modernized_learning.tsv'
	result_lab 	= 'result/modernized_learning_labeled.tsv'

	# initialize data
	print('initializing data')
	wiki 		= {old:new for (old, new) in [line.rstrip().split('\t') for line in open(wiki, 'r', encoding = 'utf8')]}
	modern 		= {line.strip() for line in open(modern, 'r', encoding = 'utf8')}

	# generate data
	print('generating learning and test data')
	learn, test = generate_data(corpus, ratio = ratio)
	baseline 	= [(old, old, new) for (old, new) in test]

	# modernize
	print('modernizing test data using wikisource')
	modern_wiki = modernize(test, modern, wiki, rules = False)
	print('modernizing test data using rules')
	modern_rule = modernize(test, modern, learn, rules = True)

	# save results
	lst_to_tsv(modern_wiki, result_base)
	lst_to_tsv(modern_rule, result_rule)

	# label missing rules
	label_rules(modern_rule, result_lab)

	# evaluate
	print('evaluating results')
	cacc_base, wacc_base = evaluate(baseline)
	cacc_wiki, wacc_wiki = evaluate(modern_wiki)
	cacc_rule, wacc_rule = evaluate(modern_rule)

	# print results
	print('---')
	print(f'baseline\ncacc = {cacc_base * 100}\nwacc = {wacc_base * 100}')
	print('---')
	print(f'using wikisource\ncacc = {cacc_wiki * 100}\nwacc = {wacc_wiki * 100}')
	print('---')
	print(f'using rules\ncacc = {cacc_rule * 100}\nwacc = {wacc_rule * 100}')
	print('---')

def generate_data(corpus, ratio = 0.5):
	learn = {}
	test = []
	files = [f for f in glob.glob(corpus + '/*.tsv')]

	for file_no, filename in enumerate(files, start = 1):
		with open(filename, 'r', encoding = 'utf8') as file:

			# calculate ratio (odd : learn_ratio, even : 1 - learn_ratio)
			learn_ratio = abs(ratio - (not file_no % 2))
			# get total number of lines
			nb_lines = sum(1 for line in file)
			# rewind
			file.seek(0)

			for line_no, line in enumerate(file.readlines(), start = 1):			
				(old, new) = line.rstrip().split('\t')

				# odd numbered file
				if (file_no % 2):
					# first part to learning dictionary
					if line_no <= nb_lines * learn_ratio:
						learn[old] = new
					# second part to test
					else:
						test.append((old, new))

				# even numbered file
				else: 
					# first part to test
					if line_no <= nb_lines * learn_ratio:
						test.append((old, new))
					# second part to learning dictionary
					else:
						learn[old] = new

	return learn, test


def modernize(test, modern_dic, learning_dic, rules = True):
	result = []
	for (old, new) in test:
		mod = old
		# old present in modern dic : keep
		if old in modern_dic:
			pass
		# old present in learning dic : apply learning dic
		elif old in learning_dic:
			mod = learning_dic[old]
		# old absent in both dics : apply rules
		elif rules:
			mods = apply_rules(old)
			# check all modernizations
			# keep the one that appears in modern dic
			mod = mods[0]
			if mod not in modern_dic:
				for m in mods[1:]:
					if m.lower() in modern_dic:
						mod = m
						break
		# store result
		result.append((old, mod, new))
	return result


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

	return mods


def label_rules(result, filename):
	with open(filename, 'w', encoding = 'utf8') as file:
		for (old, mod, new) in result:
			if mod == new:
				continue
			mod, new = align_chars(mod, new, submat = init_submat_chars())
			rules = [(o, n, rules) for o, n, rules in find_diffs(mod, new)[1]]
			mod = mod.replace('¤','')
			new = new.replace('¤','')
			file.write(f'{old}\t{mod}\t{new}\t{rules}\n')


def evaluate(result):
	wer = sum(metrics.calculate_wer(new, mod) for (old, new, mod) in result) / len(result)
	cer = sum(metrics.calculate_cer(new, mod) for (old, new, mod) in result) / len(result)
	return (1 - cer), (1 - wer)


if __name__ == '__main__':
	run()
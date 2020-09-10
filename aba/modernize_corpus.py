import re
import glob

from .utils.modern import find_diffs, modernize
from .utils.strings import cacc, wacc, align_chars, init_submat_chars
from .utils.saving import lst_to_tsv


def run():

	# parameters
	ratio 		= 0.6

	# paths
	modern 		= 'data/dic_morphalou.tsv'
	name_dic	= 'data/dic_resources.txt'
	wiki 		= 'data/dic_wikisource.tsv'
	corpus 		= 'data/PARALLEL17_aligned'
	result_base = 'result/modernized_baseline.tsv'
	result_rule = 'result/modernized_learning.tsv'
	result_lab 	= 'result/modernized_learning_labeled.tsv'

	# initialize data
	print('initializing data')
	wiki 		= {old:new for (old, new) in [line.rstrip().split('\t') for line in open(wiki, 'r', encoding = 'utf8')]}
	modern 		= {line.strip() for line in open(modern, 'r', encoding = 'utf8')}
	name 		= {line.strip() for line in open(name_dic, 'r', encoding = 'utf8')}

	# generate data
	print('generating learning and test data')
	learn, test = generate_data(corpus, ratio = ratio)
	baseline 	= [(old, new) for (old, new) in test]

	# modernize
	print('modernizing test data using wikisource')
	modern_wiki = modernize_list(test, modern, wiki, name_dic = name, rules = False)
	print('modernizing test data using rules')
	modern_rule = modernize_list(test, modern, learn, name_dic = name, rules = True)

	# save results
	lst_to_tsv(modern_wiki, result_base)
	lst_to_tsv(modern_rule, result_rule)

	# label missing rules
	label_rules(modern_rule, result_lab)

	# evaluate
	print('evaluating results')
	
	result_base = [(mod, new) for (mod, new) in baseline]
	result_wiki = [(mod, new) for (old, mod, new) in modern_wiki]
	result_aba  = [(mod, new) for (old, mod, new) in modern_rule]

	# print results
	print(
		f'---'
		f'baseline\n'
		f'cacc = {cacc(result_base) * 100}\n'
		f'wacc = {wacc(result_base) * 100}\n'
		f'---'
		f'using wikisource\n'
		f'cacc = {cacc(result_wiki) * 100}\n'
		f'wacc = {wacc(result_wiki) * 100}\n'
		f'---'
		f'using rules\n'
		f'cacc = {cacc(result_aba) * 100}\n'
		f'wacc = {wacc(result_aba) * 100}\n'
		f'---')


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


def modernize_list(test, modern_dic, learning_dic, name_dic = {}, rules = True):
	result = []
	for (old, new) in test:
		mod = modernize(old, modern_dic, learning_dic, name_dic)
		result.append((old, mod, new))
	return result


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

if __name__ == '__main__':
	run()
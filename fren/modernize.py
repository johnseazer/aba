import re
import glob

from ASR_metrics import utils as metrics



def run():

	# parameters

	ratio 		= 0.6

	# files

	modern 		= 'data/dic_morphalou.tsv'
	baseline 	= 'data/dic_wikisource.tsv'
	corpus 		= 'result/PARALLEL17/corpus_tsv'
	result_base = 'result/modernized_baseline.tsv'
	result_rule = 'result/modernized_learning.tsv'

	# initialize data

	print('initializing data')

	modern 		= {line.strip() for line in open(modern, 'r', encoding = 'utf8')}
	baseline 	= {old:new for (old, new) in [line.rstrip().split('\t') for line in open(baseline, 'r', encoding = 'utf8')]}

	# generate data

	print('generating learning and test data')
	learn, test = generate_data(corpus, ratio = ratio)

	# modernize

	print('modernizing test data using baseline')
	modern_base = modernize(test, modern, baseline, rules = False)
	print('modernizing test data using rules')
	modern_rule = modernize(test, modern, learn, rules = True)

	save_result(modern_base, result_base)
	save_result(modern_rule, result_rule)

	# evaluate

	print('evaluating results')
	cacc_base, wacc_base = evaluate(modern_base)
	cacc_rule, wacc_rule = evaluate(modern_rule)

	# print results

	print('---')
	print(f'using baseline\ncacc = {cacc_base * 100}\nwacc = {wacc_base * 100}')
	print('---')
	print(f'using rules\ncacc = {cacc_rule * 100}\nwacc = {wacc_rule * 100}')
	print('---')


def generate_data(corpus, ratio = 0.5):
	learn = {}
	test = []
	files = [filename for filename in glob.glob(corpus + '/*.tsv')]

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
								# odd numbered file
				# even numbered file
				else: 
					# first part to test
					if line_no <= nb_lines * learn_ratio:
						test.append((old, new))
					# second part to learning dictionary
					else:
						learn[old] = new

	return learn, test


def modernize(test, modern, learn, rules = True):
	result = []
	for (old, new) in test:
		# old present in modern dic : keep
		if old in modern:
			mod = old
		# old present in learning dic : apply learning dic
		elif old in learn:
			mod = learn[old]
		# old absent in both dics : apply rules
		elif rules:
			mod = apply_rules(old)
		else:
			mod = old
		# store result
		result.append((old, new, mod))
	return result


def apply_rules(s):

	# ancient characters
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

	s = re.sub('oing$', 'oin', s)

	s = re.sub('y$','i', s)
	s = re.sub('sch','ch', s)

	# verbe scavoir
	s = re.sub(r'^([Ss])ç', r'\1', s)
	s = re.sub(r'^scau', r'sau', s)

	# terminaison de verbe
	
	s = re.sub(r'([md])ens$', r'\1ents', s)
	s = re.sub(r'([fr])ens$', r'\1ends', s)

	s = re.sub(r'([ao])ye$', r'\1ie', s)
	s = re.sub(r'(.{2,})oi([st])$', r'\1ai\2', s)
	s = re.sub(r'(.{2,})oient$', r'\1aient', s)

	return s


def evaluate(result):
	wer = sum(metrics.calculate_wer(new, mod) for (old, new, mod) in result) / len(result)
	cer = sum(metrics.calculate_cer(new, mod) for (old, new, mod) in result) / len(result)
	return (1 - cer), (1 - wer)


def save_result(result, filename):
	with open(filename, 'w', encoding = 'utf8') as f:
		for (old, new, mod) in result:
			if new != mod:
				f.write(f'{old}\t{new}\t{mod}\n')



if __name__ == '__main__':
	run()
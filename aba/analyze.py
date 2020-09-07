from pathlib import Path
from pygit2 import clone_repository

from .strings.alignment import needleman_wunsch
from .strings.nlptools import preprocess, align_compound_words, align_chars, find_diffs
from .strings import substitution

from .data.saving import pairs_to_file,  pair_to_dic, dic_to_file


def run():

	# set names
	aligned_corpus_name = 'PARALLEL17_aligned'
	raw_dic_name = 'dic_p17.tsv'
	lab_dic_name = 'dic_p17_labeled.tsv'

	# set paths
	corpus_path = Path('download/PARALLEL17/corpus_tsv')
	data_path = Path('data')

	aligned_corpus_path = data_path / aligned_corpus_name
	raw_dic_path = data_path / raw_dic_name
	lab_dic_path = data_path / lab_dic_name

	# check corpus
	if not corpus_path.exists():
		print('Corpus not found. Please download PARALLEL17.')
		return

	# create required folders if needed
	data_path.mkdir(parents = True, exist_ok = True)
	aligned_corpus_path.mkdir(parents = True, exist_ok = True)

	# analyze corpus
	align_words(corpus_path, aligned_corpus_path)
	extract_dict(aligned_corpus_path, raw_dic_path)
	label_dict(raw_dic_path, lab_dic_path)


def align_words(input_dir, output_dir):

	# init substitution matrix
	submat = substitution.init_submat_chars()

	# get input files
	files = [f.name for f in input_dir.iterdir() if f.is_file() and f.suffix == '.tsv']

	# process files
	for f in files:
		print(f'processing {f}')
		# get lines from source
		with open(input_dir / f, 'r', encoding = 'utf8') as src:
			lines = src.readlines()
		# process lines and write to destination
		with open(output_dir / f, 'w', encoding = 'utf8') as dst:
			# process source file lines
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
				old = preprocess(old)
				new = preprocess(new)
				# align words with needleman-wunsch
				(old, new) = needleman_wunsch(old, new, submat = submat, mode = 'words')
				# post-process sequences
				(old, new) = align_compound_words(old, new)
				# write to file
				pairs_to_file(old, new, dst)


def extract_dict(input_dir, output_file, delta_only = True):
	
	# init dic and file list
	dic = {}
	files = [f.name for f in input_dir.iterdir() if f.is_file() and f.suffix == '.tsv']

	# process files
	for f in files:
		print(f'extracting words from {f}')
		# read file
		with open(input_dir/f, 'r', encoding = 'utf8') as src:
			lines = src.readlines()
		# process lines
		for line in lines:
			# retrieve word pair
			try:
				old, new = line.rstrip().split('\t')
			except:
				print(line)
			# add word pair to dictionary
			pair_to_dic(old, new, dic, delta_only)

	# write dic to tsv
	with open(output_file, 'w', encoding = 'utf8') as dst:
		dic_to_file(dic, dst)


def label_dict(input_file, output_file):

	submat = substitution.init_submat_chars()

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


if __name__ == '__main__':
	run()
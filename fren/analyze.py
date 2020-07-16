from pathlib import Path
from pygit2 import clone_repository

from .strings.alignment import needleman_wunsch
from .strings.nlptools import preprocess, align_compound_words, align_chars, find_diffs
from .strings import substitution

from .data.saving import pairs_to_file,  pair_to_dic, dic_to_file


def run():

	# Repository
	repo_url = 'https://github.com/e-ditiones/PARALLEL17.git'
	corpus = 'corpus_tsv'

	# Directories
	download = init_directory(Path('download'))
	result = init_directory(Path('result'))

	# Download Repository
	repo = download_repo(repo_url, download)

	# Align Words
	align_words(download/repo/corpus, result/repo/corpus)

	# Extract Dictionary
	dic = extract_dict(result/repo/corpus, result/repo)

	# Analyze Dictionary
	dic_labeled = label_dict(dic, result/repo/'dic_labeled.tsv')


def init_directory(directory):
	if not Path.exists(directory):
		directory.mkdir(parents = True)
		print(f'{directory} directory created')
	else:
		print(f'{directory} directory found')
	return directory


def download_repo(repo_url, download_dir):
	'''Downloads GitHub repo in download directory

	Returns relative path to the downloaded directory
	'''

	# parse repository name and set repository directory
	repo_name = repo_url.split('/')[-1].split('.')[0]
	repo_dir = download_dir / repo_name
	
	# return if repository already downloaded
	if Path.exists(repo_dir):
		print(f'{repo_name} already downloaded to {repo_dir}')
		return repo_name
	
	# download repository
	print(f'Download {repo_name} from {repo_url}')
	clone_repository(repo_url, repo_dir)
	print(f'{repo_name} downloaded to {repo_dir}')
	return repo_name


def align_words(input_dir, output_dir):

	if Path.exists(output_dir):
		print(f'{input_dir} already aligned, result in {output_dir}')
		return output_dir

	init_directory(output_dir)

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


def extract_dict(input_dir, output_dir, delta_only = True):

	dict_name = 'dictionary'
	dict_path = output_dir/(dict_name+'.tsv')

	# init dictionary
	dic = {}

	# init file list
	files = [f.name for f in input_dir.iterdir() if f.is_file() and f.suffix == '.tsv']

	# process all files
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
	print(f'write dictionary to {dict_path}')
	with open(dict_path, 'w', encoding = 'utf8') as dst:
		dic_to_file(dic, dst)
	
	return dict_path


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
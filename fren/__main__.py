
from pathlib import Path
from pygit2 import clone_repository

from .align import needlemanwunsch
from .align import substitution
from .align.nlptools import preprocess, align_compound_words, pairs_to_file


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
		return repo_dir
	
	# download repository
	print(f'Download {repo_name} from {repo_url}')
	clone_repository(repo_url, repo_dir)
	print(f'{repo_name} downloaded to {repo_dir}')
	return repo_dir


def align_words(input_dir, output_dir):

	'''
	if Path.exists(output_dir):
		print(f'{input_dir} already aligned, result in {output_dir}')
		return output_dir
	'''

	init_directory(output_dir)

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
				# ignore empty lines
				if (len(sequences) < 2):
					print(f'\tcorpus error : bad line format\t{sequences}')
					continue
				# unpack sequences
				old, new = sequences
				# pre-process sequences
				old = preprocess(old)
				new = preprocess(new)	
				# align words with needleman-wunsch
				old, new = needlemanwunsch.align(old, new)
				# post-process sequences
				old, new = align_compound_words(old, new)
				# write to file
				pairs_to_file(old, new, dst)
'''
'''


def run():

	# Directories
	download_dir_name = 'download'
	result_dir_name = 'result'

	download_dir = init_directory(Path(download_dir_name))
	result_dir = init_directory(Path(result_dir_name))

	# Repository
	repo_url = 'https://github.com/e-ditiones/PARALLEL17.git'
	corpus_repo_dir = 'corpus_tsv'

	# Download PARALLEL17
	repo_dir = download_repo(repo_url, download_dir)
	
	corpus_dir = repo_dir.relative_to(download_dir) / corpus_repo_dir
	input_dir = download_dir / corpus_dir
	output_dir = result_dir / corpus_dir

	# Align Words
	align_words(input_dir, output_dir)


if __name__ == '__main__':
	run()
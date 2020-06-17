from os import listdir, mkdir
from os.path import exists, isfile, join
from shutil import rmtree
from nlptools import preprocess, needleman_wunsch, align_compound_words, pairs_to_file

# define source and destination directories
src_dir = 'PARALLEL17/corpus_tsv'
dst_dir = 'corpus_tsv_aligned'

# create destination directory
if exists(dst_dir):
	rmtree(dst_dir)
if not exists(dst_dir):
	mkdir(dst_dir)

def run():

	# init source files list
	files = [f for f in listdir(src_dir) if isfile(join(src_dir, f))]

	# process files
	for f in files:
		# print current file name
		print(f)
		# get lines from source
		with open(join(src_dir, f), 'r', encoding = 'utf8') as src:
			lines = src.readlines()
		# process lines and write to destination
		with open(join(dst_dir, f), 'w', encoding = 'utf8') as dst:
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
				old, new = needleman_wunsch(old, new)
				# post-process sequences
				old, new = align_compound_words(old, new)
				# write to file
				pairs_to_file(old, new, dst)

if __name__ == '__main__':
	run()
from os import listdir, mkdir
from os.path import exists, isfile, join
from shutil import rmtree
from nlptools import preprocess, needleman_wunsch, align_compound_words, pairs_to_file

'''
main
'''

# source and destination directories
src_dir = 'PARALLEL17/corpus_tsv'
dst_dir = 'corpus_tsv_aligned'

# create destination directory
if not exists(dst_dir):
	mkdir(dst_dir)

# init source files list
files = [f for f in listdir(src_dir) if isfile(join(src_dir, f))]

# process files
for f in files:
	
	# print current file name
	print(f)
	
	# open source and destination files
	src = open(join(src_dir, f), 'r', encoding = 'utf8')
	dst = open(join(dst_dir, f), 'w', encoding = 'utf8')
	
	# process source file lines
	for line in src.readlines():

		# split line
		seqs = line.rstrip().split('\t')

		# ignore empty lines
		if (len(seqs) < 2):
			print('\t' + 'corpus error : bad line format')
			print('\t\t' + line)
			continue

		# store
		old, new = seqs
		
		# pre-process sequences
		old = preprocess(old)
		new = preprocess(new)
		
		# align words with needleman-wunsch
		old, new = needleman_wunsch(old, new)
		
		# post-process sequences
		old, new = align_compound_words(old, new)
		
		# write to file
		pairs_to_file(old, new, dst)
		
	# close files
	dst.close()
	src.close()
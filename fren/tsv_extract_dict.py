from os import listdir
from os.path import isfile, join
from nlptools import pair_to_dic, dic_to_file

delta_only = True

src_dir = 'corpus_tsv_aligned'
dic_name = 'dic_align_count'
dic_filename = dic_name + '.tsv'

# init dictionary
dic = {}

# init file list
files = [f for f in listdir(src_dir) if isfile(join(src_dir, f))]

# process all files
for f in files:

	# print current file name

	# open source file
	print('process ' + str(f))
	src = open(join(src_dir, f), 'r', encoding = 'utf8')

	# process source file lines
	for line in src.readlines():

		# retrieve word pair
		old, new = line.rstrip().split('\t')

		# add word pair to dictionary
		pair_to_dic(old, new, dic, delta_only)
	
	# close source file
	src.close()

# write dic to tsv
print('write dic to ' + dic_filename)
dst = open(dic_filename, 'w', encoding = 'utf8')
dic_to_file(dic, dst)
dst.close()
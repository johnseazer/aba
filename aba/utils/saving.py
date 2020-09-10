import glob


def pair_to_dic(old, new, dic, delta_only = False):	
	# delta only : ignore identical words
	if (delta_only and old == new):
		return
	# pair already in dic : increment count
	if old in dic and new in dic[old]:
		dic[old][new] += 1
	# pair not in dic : add to dic
	else:
		dic[old] = {new: 1}


def dic_to_file(dic, file):
	with open(file, 'w', encoding = 'utf8') as f:
		for old in dic:
			for new in dic[old]:
				f.write(f'{old}\t{new}\t{dic[old][new]}\n')


def lst_to_tsv(lst, file):
	open(file, 'w', encoding = 'utf8').write('\n'.join(['\t'.join(e) for e in lst]))


def extract_dic(src_dir, dst_file, delta_only = True):
	
	# init dic and file list
	dic = {}
	files = [f for f in glob.glob(src_dir + '/*.tsv')]

	# process files
	for f in files:
		print(f'Extracting words from {f}...')
		# read file
		lines = open(f, 'r', encoding = 'utf8').readlines()
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
	dic_to_file(dic, dst_file)
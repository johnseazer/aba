def pairs_to_file(a, b, dst, delta_only = False):
	'''
	takes two same-sized lists of strings a and b
	writes each pair of corresponding strings as a line to dst in tsv format
	'''
	assert len(a) == len(b), 'different list sizes'
	# go through each pair of corresponding words
	for old, new in zip(a, b):
		# ignore pairs of identical words if delta only
		if (delta_only and old == new):
			continue
		# write pair of corresponding words to file in tsv format
		dst.write(old + '\t' + new + '\n')


def pair_to_dic(old, new, dic, delta_only = False):	
	'''
	takes two strings old and new
	adds the pair to dictionary dic as follows :
	- keys are strings from old
	- values are dictionaries in which :
		- keys are strings from new
		- values are the count of (old, new) occurences
	'''
	# delta only : ignore identical words
	if (delta_only and old == new):
		return
	# pair already in dic : increment count
	if old in dic and new in dic[old]:
		dic[old][new] += 1
	# pair not in dic : add to dic
	else:
		dic[old] = {new: 1}


def dic_to_file(dic, f):
	'''
	write dictionary to tsv
	format : old, new, count
	'''
	for old in dic:
		for new in dic[old]:
			count = dic[old][new]
			f.write(old + '\t' + new + '\t' + str(count) + '\n')

def lst_to_tsv(lst, filename, delta_only = False):
	with open(filename, 'w', encoding = 'utf8') as f:
		for e in lst:
			entry = str(e).strip('()').replace(', ','\t').replace("'",'') + '\n'
			f.write(entry)
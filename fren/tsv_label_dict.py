from nlptools import align_chars, get_diffs

# filenames
src_name = 'dic_align_count'
dst_name = 'dic_label'

# functions

def run():
	# read entries from source dictionary
	with open(f'{src_name}.tsv', 'r', encoding = 'utf8') as src:
		lines = src.readlines()
	# process entries
	with open(f'{dst_name}.tsv', 'w', encoding = 'utf8') as dst:
		# process dictionary entries
		for line in lines:
			# parse entry
			old, new, count = line.rstrip('\n').split('\t')
			# align chars
			old, new = align_chars(old, new)
			# find differences
			ndiffs, diffs = get_diffs(old, new)
			# write new entry for each diff
			for diff in diffs:
				old_chars, new_chars, rules = diff
				dst.write(f'{old}\t{new}\t{count}\t{ndiffs}\t{old_chars}\t{new_chars}\t{rules}\n')

# main
if __name__ == '__main__':
	run()
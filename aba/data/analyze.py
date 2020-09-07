def get_rules(input, output):

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
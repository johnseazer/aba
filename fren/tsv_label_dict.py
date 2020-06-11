from nlptools import align_chars, get_diffs

# filenames
src_name = 'dic_align_count'
dst_name = 'dic_label'

# open dic
src = open(src_name + '.tsv', 'r', encoding = 'utf8')
dst = open(dst_name + '.tsv', 'w', encoding = 'utf8')

# process dictionary entries
for line in src.readlines():
	
	# parse entry
	old, new, count = line.rstrip('\n').split('\t')
	
	# align chars
	old, new = align_chars(old, new)
	
	# find differences
	diffs = get_diffs(old, new)
	
	# no differences found
	if diffs == []:
		# write entry, empty diff
		dst.write(old + '\t' +
				   new + '\t' +
				   count + '\t' +
				   '\t' +
				   '\t' +
				   '\n')

	# differences found
	else:
		# write entry for each diff
		for diff in diffs:
			dst.write(old + '\t' +
					   new + '\t' +
					   count + '\t' +
					   diff[0] + '\t' +
					   diff[1] + '\t' +
					   diff[2] + '\n')

src.close()
dst.close()
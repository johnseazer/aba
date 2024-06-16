import argparse
import glob
import os
from os import walk

default_dir = os.path.join(os.path.join('download','FreEMnorm'),'corpus')

parser = argparse.ArgumentParser()
parser.add_argument('old', type = str,
	help = 'old string to search')
parser.add_argument('new', type = str,
	help = 'new string to search')
parser.add_argument('-d', '--directory', type = str,
	help = 'searching directory',
	default = default_dir)
args = parser.parse_args()

# get list of files in directory
#files = [f for f in os.path.join(glob.glob(args.directory, '*.tsv'))]
f = []
for (dirpath, dirnames, filenames) in walk(args.directory):
    f.extend(filenames)
print(f)

# read each file
for file in f:
	filename = os.path.basename(file)
	filename_printed = True
	# get lines from file
	lines = [line.strip() for line in open(os.path.join(default_dir,file), 'r', encoding = 'utf8')]
	# search lines
	for line_no, line in enumerate(lines):
		# split line
		split_line = line.split('\t')
		if len(split_line) != 2:
			# bad format
			old = new = line
		else:
			# good format
			old, new = split_line
		# search strings
		if args.old in old and args.new in new:
			if not filename_printed:
				print (f'{filename}')
				filename_printed = True
			print(f'{filename} \t {(line_no + 1):4} \t  {line}')
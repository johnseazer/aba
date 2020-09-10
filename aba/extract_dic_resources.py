# Script to extract dictionary from multiple `.dic` files in the same folder

import glob
import argparse

default_src_dir = 'resources'
default_dst_dir = 'data'
default_dst_filename = 'dic_resources'

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--src_dir', type = str,
	help = 'source directory for .dic files',
	default = default_src_dir)
parser.add_argument('-d', '--dst_dir', type = str,
	help = 'destination directory for dictionary file',
	default = default_dst_dir)
parser.add_argument('-f', '--dst_filename', type = str,
	help = 'filename for dictionary file',
	default = default_dst_filename)

args = parser.parse_args()

# get list of .dic files in directory
files = [f for f in glob.glob(args.src_dir + '/*.dic')]

# fill dictionary
dic = []
for f in files:
	print(f'Extracting words from {f}...')
	dic.extend([line.split(',')[0] for line in open(f, 'r', encoding = 'utf8')])

filepath = args.dst_dir + '/' + args.dst_filename + '.txt'
print(f'Saving to {filepath}...')
open(filepath, 'w', encoding = 'utf8').write('\n'.join(dic))
print('Done.')
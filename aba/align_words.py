import os
import glob
import argparse

from .utils.strings import align_words
from .utils.saving import extract_dict
from .utils.modern import label_dict


def run():

	default_src_dir = 'download/PARALLEL17/corpus_tsv'
	default_dst_dir = 'data/PARALLEL17_words'

	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--src_dir', type = str,
		help = 'source directory for .dic files',
		default = default_src_dir)
	parser.add_argument('-d', '--dst_dir', type = str,
		help = 'destination directory for dictionary file',
		default = default_dst_dir)
	args = parser.parse_args()

	if not os.path.exists(args.dst_dir):
		os.makedirs(args.dst_dir)

	files = [f for f in glob.glob(args.src_dir + '/*.tsv')]

	for file in files:
		filename = file.split('\\')[-1]
		print(f'Aligning {filename} by words...')
		al = align_words(file)
		open(args.dst_dir + '/' + filename, 'w', encoding = 'utf8').write('\n'.join(['\t'.join(words) for words in al]))

if __name__ == '__main__':
	run()
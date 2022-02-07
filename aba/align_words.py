import os
import glob
import argparse

from .utils.strings import align_words
from .utils.saving import lst_to_tsv

def run():

	default_src_dir = os.path.join(os.path.join('download','PARALLEL17'),'corpus_tsv')
	default_dst_dir = os.path.join('data','PARALLEL17_words')

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

	files = [f for f in glob.glob(os.path.join(args.src_dir, '*.tsv'))]

	for file in files:
		filename = os.path.basename(file)
		filepath = os.path.join(args.dst_dir, filename)
		print(f'Aligning {filename} by words...')
		aligned_words = align_words(file)
		lst_to_tsv(aligned_words, filepath)
		
if __name__ == '__main__':
	run()